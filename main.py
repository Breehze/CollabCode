from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, WebSocketDisconnect, WebSocket 
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import  CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.wsmanager import ConManager 
from utils import docOperations
from utils import containerManager
from uuid import uuid4

"""
operation : insert/delete/nline
cord : (x,y)
content : letter
}
""" 
DOMAIN = "127.0.0.1:8000"
cont_manager = containerManager.containerManager({'python:3.11-slim': 2})
test_docs = {}

templates = Jinja2Templates("templates")
vue_build = Jinja2Templates("messin_round/dist")

con_man = ConManager()


@asynccontextmanager
async def lifespan(app : FastAPI):
    print("start up")
    yield
    cont_manager.teardown()
    
app = FastAPI(lifespan = lifespan)

origins = ["http://localhost:5173"] #dev purposes

app.add_middleware(CORSMiddleware,allow_origins= origins,allow_credentials=True,allow_methods=['*'],allow_headers= ['*'])
app.mount("/assets",StaticFiles(directory='messin_round/dist/assets'))


@app.get("/")
async def landing_page(request:Request):
    #collab_uuid = str(uuid4())
    #test_docs.update({collab_uuid: [[]]}) 
    #collab_url = f"http://{DOMAIN}/collab?col_id={collab_uuid}"  
    #return templates.TemplateResponse("landing_page.html",{"request": request, "collab_url" : collab_url})
    return vue_build.TemplateResponse("index.html",{'request' : request})

@app.get("/collab")
async def collab_page(request : Request,col_id : str):
    #if col_id not in test_docs:
    #    raise HTTPException(status_code=404 , detail="This collab couldn't be found")
    #return  templates.TemplateResponse("test.html",{"request": request, "DOMAIN" : DOMAIN,"collab_id":col_id})
    return vue_build.TemplateResponse("index.html",{"request" : request})

@app.get("/generate_collab")
async def generate_collab_id():
    collab_uuid = str(uuid4())
    test_docs.update({collab_uuid: [[]]})
    return collab_uuid 

@app.post("/run/{collab_doc_id}")
async def run_py(collab_doc_id : str):
    if collab_doc_id not in test_docs:
        raise HTTPException(status_code=400,detail="This collab doesn't exist")
    merged = '\n'.join([''.join(inner_list) for inner_list in test_docs[collab_doc_id]])
    return await cont_manager.run_code_async("python:3.11-slim",merged) 

@app.websocket("/collab/{live_collab_id}")
async def hello_socket(ws : WebSocket, live_collab_id : str ):
    """Get the doc -> send doc to clients -> wait for insertions -> manage conflicts -> update the doc -> wait for ins..."""
    ws_doc = test_docs[live_collab_id]
    
    await con_man.connect(live_collab_id,ws)
    await con_man.send_personal_message(ws_doc,ws)
    try:
        while True:
            content_rec = await ws.receive_json()
            match content_rec["operation"]: 
                case "Nline":
                    docOperations.new_line(ws_doc,content_rec) 
                case "Delete":
                    docOperations.letter_delete(ws_doc,content_rec)
                case "Paste":
                    docOperations.paste(ws_doc,content_rec)
                case _:
                    docOperations.letter_insert(ws_doc,content_rec)
 
            print(ws_doc)
            await con_man.broadcast(ws,live_collab_id,content_rec) 
    except:
        con_man.disconnect(live_collab_id,ws)
        if live_collab_id not in con_man.active_connections:
            test_docs.pop(live_collab_id)

