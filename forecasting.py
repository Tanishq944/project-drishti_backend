# forecasting.py
from google.cloud import firestore
import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv
load_dotenv()

COLL = "camera_metrics"  # same as used earlier
firestore_client = firestore.Client()

def load_recent_series(zone_id, minutes=120):
    # load data for the last N minutes
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    q = firestore_client.collection(COLL).where('zone_id', '==', zone_id).where('timestamp', '>=', cutoff.isoformat()).order_by('timestamp')
    rows = [r.to_dict() for r in q.stream()]
    if not rows:
        return None
    df = pd.DataFrame(rows)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[['timestamp','person_count']].rename(columns={'timestamp':'ds','person_count':'y'})
    return df

def forecast_zone(zone_id, predict_minutes=20, frequency='min'):
    df = load_recent_series(zone_id, minutes=180)  # last 3 hours
    if df is None or len(df) < 10:
        return None
    # resample to 1-minute frequency to unify time series
    df = df.set_index('ds').resample('1T').mean().interpolate()
    df = df.reset_index()
    m = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False)
    m.fit(df)
    periods = int(predict_minutes)
    future = m.make_future_dataframe(periods=periods, freq='min')
    forecast = m.predict(future)
    # return only the forecast window
    fc = forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(periods)
    # convert to list
    return fc.to_dict(orient='records')

# quick runner
if __name__ == "__main__":
    zone = "west_zone"
    fc = forecast_zone(zone, predict_minutes=20)
    print(fc)
