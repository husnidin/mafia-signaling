import socketio
from fastapi import FastAPI, Request
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

# Har bir room uchun foydalanuvchilar ro'yxati
rooms = {}

@sio.event
async def connect(sid, environ):
    print("Connected:", sid)

@sio.event
async def disconnect(sid):
    for room_id, users in rooms.items():
        if sid in users:
            print(f"Disconnected {sid} from {room_id}")
            users.remove(sid)

@sio.event
async def join_room(sid, room):
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(sid)
    print(f"{sid} joined {room}")
    await sio.emit("all-users", [s for s in rooms[room] if s != sid], room=sid)

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

# Yangi: mavjud xonalarni va foydalanuvchilarni ko‘rsatish uchun API endpoint
@app.get("/rooms")
async def get_rooms():
    return {"rooms": rooms}
