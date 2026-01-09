# backend/vertex_predict.py
import pandas as pd, os
from datetime import timedelta
from google.cloud import aiplatform

def _load_recent(csv_path, minutes=60):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").tail(minutes)  # last N rows ~ minutes
    # minimal features for AutoML Forecasting online predict
    return df[["camera_id","timestamp","people_count"]]

def forecast_with_vertex(csv_path, project, location, endpoint_id, minutes=20):
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)

    hist = _load_recent(csv_path, minutes=60)
    cam = hist["camera_id"].iloc[-1]
    last_ts = hist["timestamp"].iloc[-1]
    rows = []
    for _, r in hist.iterrows():
        rows.append({"camera_id": r["camera_id"], "timestamp": r["timestamp"].isoformat(), "people_count": float(r["people_count"])})
    # For AutoML Forecasting, send the recent context rows (no future target)
    instance = {"time_series_identifier": cam, "rows": rows}
    pred = endpoint.predict(instances=[instance])
    # take the median/point forecast for ~minutes horizon
    # Different models return slightly different structures; pick first value.
    val = float(pred.predictions[0].get("value", pred.predictions[0]))
    return {"source":"vertex","forecast_people_count": val}
