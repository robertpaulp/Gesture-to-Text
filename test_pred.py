from gesture_recognizer import GestureRecognizer
import cv2
import asyncio
import os

gesture_recognizer = GestureRecognizer()

TEST_DIR_PATH = "virtual_camera_imgs"

# Get all image files from the directory
image_files = [f for f in os.listdir(TEST_DIR_PATH) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for image_file in image_files:
    image_path = os.path.join(TEST_DIR_PATH, image_file)
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        continue

    # Process the loaded image
    prediction = gesture_recognizer.process_image(image)
    print(f"Image: {image_file}, Predicted gesture: {prediction}")