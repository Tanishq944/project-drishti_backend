import time
import random
import uuid
from datetime import datetime
from google.cloud import bigquery

# -------------------------------
# CONFIG
# -------------------------------
PROJECT_ID = "project-drishti-468209"
TABLE_ID = "project-drishti-468209.crowd_metrics.frame_analysis"

# -------------------------------
# BIGQUERY CLIENT
# -------------------------------
client = bigquery.Client(project=PROJECT_ID)

def log_to_bigquery(people_count, density, anomaly_detected):
    """Insert a single row into BigQuery"""
    row = {
        "frame_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "people_count": people_count,
        "density": density,
        "anomaly_detected": anomaly_detected,
    }

    errors = client.insert_rows_json(TABLE_ID, [row])
    if errors:
        print(f"❌ BigQuery Insert Errors: {errors}")
    else:
        print(f"✅ Logged to BigQuery: {row}")

# -------------------------------
# MAIN LOOP (Dummy Data Generator)
# -------------------------------
def main():
    while True:
        # Generate dummy crowd metrics
        people_count = random.randint(10, 500)
        density = round(random.uniform(0.1, 5.0), 2)
        anomaly_detected = people_count > 400 or density > 4.0

        # Log to BigQuery
        log_to_bigquery(people_count, density, anomaly_detected)

        # Wait 10 seconds before next entry
        time.sleep(10)

if __name__ == "__main__":
    main()
