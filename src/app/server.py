import uvicorn
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
def read_root():
    return {"message": "Tic Tac Toe Server is running"}


# Add a function to start the server
def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # Start the FastAPI server in a new thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
