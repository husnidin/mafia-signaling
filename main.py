import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = FastAPI()
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms = {}

@sio.event
async def connect(sid, environ):
    print("Connected:", sid)

@sio.event
async def disconnect(sid):
    for room in rooms.values():
        if sid in room:
            room.remove(sid)

@sio.event
async def join_room(sid, room):
    if room not in rooms:
        rooms[room] = []
    users_in_room = rooms[room]
    rooms[room].append(sid)
    await sio.emit("all-users", users_in_room, room=sid)

@sio.event
async def send_signal(sid, data):
    await sio.emit("user-joined", {
        "signal": data["signal"],
        "callerID": data["callerID"]
    }, room=data["userToSignal"])

@sio.event
async def return_signal(sid, data):
    await sio.emit("receiving-returned-signal", {
        "signal": data["signal"],
        "id": sid
    }, room=data["callerID"])
