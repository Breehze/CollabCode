from fastapi import WebSocket
from uuid import uuid4

class ConManager:
    def __init__(self):
        self.active_connections: dict[str,list[WebSocket]] = {}

    async def connect(self, uuid : str, websocket: WebSocket):
        await websocket.accept()
        if uuid not in self.active_connections:
            self.active_connections.update({uuid:[websocket]})
        else:
            self.active_connections[uuid].append(websocket)
        print(self.active_connections)
    def disconnect(self,uuid : str, websocket: WebSocket):
        if len(self.active_connections[uuid]) <= 1:
            self.active_connections.pop(uuid)
        else:
            self.active_connections[uuid].remove(websocket)
        print(self.active_connections)

    async def send_personal_message(self, message: list | dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self,client_ws,uuid : str, message : list | dict):
        for connection in self.active_connections[uuid]:
            if connection == client_ws:
                continue
            await connection.send_json(message)


