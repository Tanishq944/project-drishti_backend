from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import time

app = FastAPI()

# ✅ Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "✅ Project Drishti backend is running!"}


# ✅ Load YOLO model (keep this file in same directory or adjust path)
model = YOLO("yolov8n.pt")

last_frame_time = None
last_person_count = 0


@app.post("/process_frame")
async def process_frame(file: UploadFile = File(...)):
    """
    Endpoint to process each frame sent from frontend.
    Returns person count, density, and speed.
    """
    global last_frame_time, last_person_count

    try:
        # Read uploaded image
        image = await file.read()
        npimg = np.frombuffer(image, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # YOLO object detection
        results = model(frame, verbose=False)
        boxes = results[0].boxes

        # Count people (class 0 = person)
        person_count = sum(1 for box in boxes if int(box.cls[0]) == 0)

        # Compute density and speed
        h, w = frame.shape[:2]
        density = round(person_count / (h * w) * 10000, 4)

        current_time = time.time()
        speed = 0
        if last_frame_time is not None:
            speed = abs(person_count - last_person_count) / (current_time - last_frame_time)

        last_person_count = person_count
        last_frame_time = current_time

        return {
            "status": "success",
            "person_count": person_count,
            "density": density,
            "speed": round(speed, 3),
        }

    except Exception as e:
        print("❌ Error processing frame:", e)
        return {"status": "error", "message": str(e)}
