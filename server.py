import asyncio
import websockets
import json

async def gesture_server(websocket):
    try:
        # For testing, send a message every 3 seconds
        while True:
            message = json.dumps({"text": "Test caption message"})
            await websocket.send(message)
            await asyncio.sleep(3)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(gesture_server, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())