# processing.py  ✅ FIXED FOR PROJECT DRISHTI
import os, io, uuid, time
from google.cloud import storage, firestore, aiplatform
from datetime import datetime
import numpy as np
import cv2
from PIL import Image
from dotenv import load_dotenv

# -------------------- LOAD ENV --------------------
load_dotenv()

PROJECT = "project-drishti-468209"
LOCATION = "asia-south1"   # ✅ Correct region
BUCKET = os.getenv("GCS_BUCKET")
ENDPOINT = os.getenv("VERTEX_VISION_ENDPOINT")  # must be full endpoint path
COLL = "camera_metrics"
ALERT_THRESHOLD = int(os.getenv("ALERT_THRESHOLD", "15"))

# -------------------- GOOGLE CLOUD INIT --------------------
storage_client = storage.Client()
firestore_client = firestore.Client()

aiplatform.init(project=PROJECT, location=LOCATION)
vision_endpoint = aiplatform.Endpoint(endpoint_name=ENDPOINT)

_last_frames = {}

# -------------------- UPLOAD TO GCS --------------------
def upload_to_gcs(image_bytes, camera_id):
    filename = f"frames/{camera_id}/{int(time.time())}_{uuid.uuid4().hex[:8]}.jpg"
    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type="image/jpeg")
    return f"gs://{BUCKET}/{filename}"

# -------------------- VERTEX AI PREDICT --------------------
def call_vertex_vision(gcs_uri):
    instances = [{"gcsImageUri": gcs_uri}]
    response = vision_endpoint.predict(instances=instances)
    return response

# ✅ FIXED: Proper parser for Vertex Vision object detection
def extract_persons(pred):
    persons = []

    for p in pred.predictions:
        display_names = p.get("displayNames", [])
        confidences = p.get("confidences", [])
        bboxes = p.get("bboxes", [])

        for name, score, bbox in zip(display_names, confidences, bboxes):
            if "person" in name.lower():
                persons.append({"bbox": bbox, "score": float(score)})

    return persons

# -------------------- FLOW + DENSITY --------------------
def compute_density(persons, w, h):
    count = len(persons)
    density = count / ((w * h) / 10000.0 + 1e-6)
    return count, density

def compute_optical_flow(camera_id, image_bytes):
    curr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    if curr is None:
        return 0.0

    prev = _last_frames.get(camera_id)
    avg_flow = 0.0

    if prev is not None and prev.shape == curr.shape:
        flow = cv2.calcOpticalFlowFarneback(prev, curr, None,
                                            0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        avg_flow = float(np.mean(mag))

    _last_frames[camera_id] = curr
    return avg_flow

# -------------------- SAVE TO FIRESTORE --------------------
def save_metrics(camera_id, zone_id, count, density, avg_flow, gcs_uri, lat, lon):
    doc = {
        "camera_id": camera_id,
        "zone_id": zone_id,
        "person_count": count,
        "density": density,
        "speed": avg_flow,
        "gcs_uri": gcs_uri,
        "timestamp": datetime.utcnow().isoformat(),
    }
    if lat: doc["lat"] = float(lat)
    if lon: doc["lon"] = float(lon)

    firestore_client.collection(COLL).add(doc)
    return doc

# -------------------- MAIN PROCESSOR --------------------
def process_frame(image_bytes, camera_id, zone_id, lat=None, lon=None):

    gcs_uri = upload_to_gcs(image_bytes, camera_id)

    # Call Vertex AI
    pred_resp = call_vertex_vision(gcs_uri)

    # Parse people
    persons = extract_persons(pred_resp)

    # Frame dims
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    h, w = img.shape[:2]

    count, density = compute_density(persons, w, h)
    avg_flow = compute_optical_flow(camera_id, image_bytes)

    doc = save_metrics(camera_id, zone_id, count, density, avg_flow, gcs_uri, lat, lon)

    alert = None
    if count >= ALERT_THRESHOLD:
        alert = {
            "level": "high",
            "message": f"⚠ High crowd density: {count} people detected"
        }
        firestore_client.collection("alerts").add({
            **doc,
            "alert": alert,
            "generated_at": datetime.utcnow().isoformat()
        })

    return {"ok": True, "metric": doc, "alert": alert}
