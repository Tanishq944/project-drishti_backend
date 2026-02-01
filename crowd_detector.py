import cv2
from ultralytics import YOLO
import numpy as np
from datetime import datetime
import requests

# -------------------------
# CONFIG
# -------------------------
VIDEO_PATH = "crowd_video.mp4"  # 👈 put your video in backend folder or update full path
API_URL = "http://127.0.0.1:5000/api/crowd"  # Flask backend endpoint

# Load YOLOv8 model (pre-trained COCO dataset has 'person' class)
model = YOLO("yolov8n.pt")

# Open video
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print(f"❌ Could not open video file at {VIDEO_PATH}. Check the path!")
    exit()

print("✅ Video opened successfully, starting detection...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("⚠️ End of video or cannot read frame.")
        break

    print("🎥 Reading frame...")  # Debug log

    # Run detection
    results = model(frame)

    # Filter detections for 'person' class (COCO class id = 0)
    people = [r for r in results[0].boxes if int(r.cls[0]) == 0]

    people_count = len(people)
    h, w, _ = frame.shape
    area = h * w
    density = round(people_count / (area / 10000), 2)  # rough estimate

    # Estimate velocity (skipping for now, placeholder = 0)
    velocity = 0  

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print results
    print(f"📌 {timestamp} | People: {people_count}, Density: {density}, Velocity: {velocity}")

    # Send to backend API
    try:
        payload = {
            "timestamp": timestamp,
            "people_count": people_count,
            "density": density,
            "velocity": velocity,
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("✅ Data sent to backend API")
        else:
            print(f"⚠️ Failed to send data (status {response.status_code})")
    except Exception as e:
        print(f"❌ Error sending data: {e}")

cap.release()
print("✅ Video processing complete.")
