import cv2
import requests
import time

# ✅ Correct FastAPI endpoint for raw JPEG uploads
API_URL = "http://127.0.0.1:8000/process_frame"


cam = cv2.VideoCapture(0)

print("✅ Webcam started. Press 'Q' to stop.")

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    _, img_encoded = cv2.imencode(".jpg", frame)
    files = {"file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}

    response = requests.post(URL, files=files)
    print(response.json())

    cv2.imshow("Live Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
