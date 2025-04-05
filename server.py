import asyncio
import websockets
import json
import cv2
import os
from datetime import datetime
import gesture_recognizer as gr

# === Setup ===
output_folder = "virtual_camera_imgs"
os.makedirs(output_folder, exist_ok=True)
recognizer = gr.GestureRecognizer()

CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600

# === Încearcă să deschidă camera virtuală OBS ===
def get_virtual_camera_index():
    for i in range(5):  # testăm primele 5 camere
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
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

            # Salvează imaginea curentă în folderul de ieșire
            # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # image_path = os.path.join(output_folder, f"frame_{timestamp}.jpg")
            # cv2.imwrite(image_path, frame)
            # print(f"✅ Imagine salvată: {image_path}")

            # Procesăm imaginea pentru a prezice gestul
            predicted_gesture = recognizer.process_image(frame)
            if predicted_gesture:
                print(f"Predicted gesture: {predicted_gesture}")
            else:
                print("Niciun gest detectat")

            # Trimitem un mesaj dummy prin WebSocket
            message = json.dumps({
                "text": predicted_gesture if predicted_gesture else "N/A",
            })
            await websocket.send(message)

            await asyncio.sleep(0.1)  # așteptăm 100ms între cadre

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
