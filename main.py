from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi import WebSocket 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.wsmanager import ConManager 
from uuid import uuid4

app = FastAPI()
"""
operation : insert/delete/newline
cord : (x,y)
content : letter
}
"""

example_doc = [[]]
templates = Jinja2Templates("templates")

con_man = ConManager()

@app.get("/collab")
async def collab_page(request : Request,col_id : str):
    return  templates.TemplateResponse("test.html",{"request": request})

@app.websocket("/ws/{live_collab_id}")
async def hello_socket(ws : WebSocket, live_collab_id : str ):
    """Get the doc -> send doc to clients -> wait for insertions -> manage conflicts -> update the doc -> wait for ins..."""
    await con_man.connect(live_collab_id,ws)#ws.accept()
    await con_man.send_personal_message(example_doc,ws)#ws.send_json(example_doc)
    try:
        while True:
            content_rec = await ws.receive_json()
            if content_rec["operation"] == "Nline":
                example_doc.insert(content_rec["cords"][0],[])
            elif content_rec["operation"] == "Delete":
                if len(example_doc[0]) == 0:
                    continue
                if content_rec["cords"][1] == len(example_doc[content_rec['cords'][0]]) -1:
                    example_doc.pop(content_rec["cords"][0]+1)
                else:
                    example_doc[content_rec["cords"][0]].pop(content_rec["cords"][1]+1)
            elif content_rec["operation"] == "Paste":
                cords = content_rec['cords']
                lines_copied = len(content_rec["content"])
                if lines_copied == 1:
                    example_doc[cords[0]][cords[1]+1:cords[1]+1] = content_rec["content"][0]
                    print(content_rec)
                else:
                    end = example_doc[cords[0]][cords[1] + 1:]
                    example_doc[cords[0]] = example_doc[cords[0]][:cords[1] + 1]
                    example_doc[cords[0]][cords[1]+1:cords[1]+1] = content_rec["content"][0]
                    j = 1
                    for i in range(cords[0] + 1,cords[0] + lines_copied):
                        example_doc.insert(i,content_rec["content"][j])
                        j+=1
                    example_doc[cords[0] + lines_copied-1].extend(end) 
                
            else:
                example_doc[content_rec["cords"][0]].insert(content_rec["cords"][1],content_rec["content"])
            print(example_doc)
            await con_man.broadcast(live_collab_id,content_rec) #ws.send_json(content_rec)
    except WebSocketDisconnect:
        con_man.disconnect(live_collab_id,ws)
