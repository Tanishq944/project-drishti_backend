from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import time
import json
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "models/gemini-2.5-flash"   # <-- VERIFIED valid for your key

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is running successfully!"}

# Load YOLO model
yolo = YOLO("yolov8n.pt")
last_frame_time = None
last_person_count = 0


# ------------------------------ PROCESS FRAME ------------------------------
@app.post("/process_frame")
async def process_frame(file: UploadFile = File(...)):
    global last_frame_time, last_person_count

    try:
        image_bytes = await file.read()
        npimg = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        results = yolo(frame, verbose=False, conf=0.3)
        boxes_data = []
        person_count = 0

        for b in results[0].boxes:
            cls = int(b.cls[0])
            conf = float(b.conf[0])
            x1, y1, x2, y2 = map(float, b.xyxy[0])

            if cls == 0:
                person_count += 1

            boxes_data.append({
                "cls": cls,
                "conf": round(conf, 2),
                "box": [x1, y1, x2, y2]
            })

        h, w = frame.shape[:2]
        density = round(person_count / (h * w) * 10000, 4)

        current_time = time.time()
        speed = 0
        if last_frame_time:
            speed = abs(person_count - last_person_count) / (current_time - last_frame_time)

        last_person_count = person_count
        last_frame_time = current_time

        return {
            "status": "success",
            "person_count": person_count,
            "density": density,
            "speed": round(speed, 3),
            "boxes": boxes_data
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# ------------------------- DUMMY EVENT DATA --------------------------------
def get_crowd_data(zone):
    return {"density": 68.5, "velocity": 0.45, "surge_detected": False}

def get_incidents(zone):
    return [{"type": "medical", "location": "Gate 1", "severity": "medium"}]

def get_anomalies(zone):
    return ["Smoke near Gate 2", "Slow movement near Stage A"]

def get_social_media(zone):
    return ["Long queues reported in West Zone"]

def get_weather():
    return "Clear sky, 34°C"


# ---------------------- GENERATE AI SUMMARY (REST API) ---------------------
@app.get("/generate_summary")
def generate_summary(zone: str):

    event_data = {
        "zone": zone,
        "crowd_status": get_crowd_data(zone),
        "incidents": get_incidents(zone),
        "anomalies": get_anomalies(zone),
        "social_media": get_social_media(zone),
        "weather": get_weather()
    }

    prompt = f"""
    You are DRISHTI — an AI safety assistant.
    Create a short, clear summary of this event data:
    {json.dumps(event_data, indent=2)}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/{GEMINI_MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, json=payload)
    data = response.json()

    try:
        summary = data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        summary = "Error generating summary: " + str(data)

    return {"zone": zone, "summary": summary}
