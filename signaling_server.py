import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

rooms = {}

@sio.event
async def connect(sid, environ):
    print(f"🔌 Connected: {sid}")

@sio.event
async def join_room(sid, room):
    sio.enter_room(sid, room)
    rooms.setdefault(room, []).append(sid)
    
    # Faqat yangi foydalanuvchiga boshqa userlar ro'yxatini yubor
    await sio.emit("all-users", [s for s in rooms[room] if s != sid], to=sid)


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

@sio.event
async def disconnect(sid):
    for room in rooms.values():
        if sid in room:
            room.remove(sid)
