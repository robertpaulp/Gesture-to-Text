import asyncio
import websockets
import json
import cv2
import os
from datetime import datetime
import time

# === Setup ===
output_folder = "capturi_din_virtualcam"
os.makedirs(output_folder, exist_ok=True)

# === Încearcă să deschidă camera virtuală OBS ===
def get_virtual_camera_index():
    for i in range(5):  # testăm primele 5 camere
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print(f"[✔] Găsit video stream pe indexul {i}")
                return i
    print("❌ Nu am găsit camera virtuală. Verifică dacă OBS Virtual Camera e pornită.")
    exit()

camera_index = get_virtual_camera_index()
cap = cv2.VideoCapture(camera_index)

# === WebSocket server care trimite un mesaj text ===

async def gesture_server(websocket):
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Nu pot citi din camera virtuală.")
                break

            # Salvăm imaginea
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_folder, f"frame_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[📸] Poză salvată: {filename}")

            # Trimitem un mesaj dummy prin WebSocket
            message = json.dumps({"text": f"Poză capturată la {timestamp}"})
            await websocket.send(message)

            await asyncio.sleep(2)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        cap.release()

# === Rulează serverul ===
async def main():
    async with websockets.serve(gesture_server, "localhost", 8765):
        print("✅ WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # rulează la infinit

if __name__ == "__main__":
    asyncio.run(main())
