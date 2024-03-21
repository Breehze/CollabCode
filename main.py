from fastapi import FastAPI, Request, WebSocketDisconnect, WebSocket 
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from utils.wsmanager import ConManager 
from utils import docOperations
from utils import codeExec
from uuid import uuid4

app = FastAPI()
"""
operation : insert/delete/nline
cord : (x,y)
content : letter
}
""" 

test_docs = {}
templates = Jinja2Templates("templates")

con_man = ConManager()

@app.get("/")
async def landing_page(request:Request):
    collab_uuid = str(uuid4())
    test_docs.update({collab_uuid: [[]]}) 
    collab_url = f"http://127.0.0.1:8000/collab?col_id={collab_uuid}"  
    return templates.TemplateResponse("landing_page.html",{"request": request, "collab_url" : collab_url})

@app.get("/collab")
async def collab_page(request : Request,col_id : str):
    if col_id not in test_docs:
        raise HTTPException(status_code=404 , detail="This collab couldn't be found")
    return  templates.TemplateResponse("test.html",{"request": request})

@app.post("/run/{collab_doc_id}")
async def run_py(collab_doc_id : str):
    if collab_doc_id not in test_docs:
        raise HTTPException(status_code=400,detail="This collab doesn't exist")
    merged = '\n'.join([''.join(inner_list) for inner_list in test_docs[collab_doc_id]])
    return await codeExec.run_python(merged)

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
            await con_man.broadcast(live_collab_id,content_rec) 
    except WebSocketDisconnect:
        con_man.disconnect(live_collab_id,ws)
