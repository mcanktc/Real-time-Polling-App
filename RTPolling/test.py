import asyncio
import websockets
import json

async def vote():
    uri = "ws://localhost:8000/ws/poll/1/"
    async with websockets.connect(uri) as websocket:
        data = {
            "poll_id": 1,
            "option_id": 1
        }
        await websocket.send(json.dumps(data))
        print("📨 Oy gönderildi!")

        while True:
            response = await websocket.recv()
            print("🟢 Yayın Geldi:", response)

asyncio.run(vote())
