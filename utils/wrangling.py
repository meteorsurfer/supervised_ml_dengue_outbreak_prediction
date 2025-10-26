from io import BytesIO
import pandas as pd 
import requests 
import streamlit as st
from datetime import timedelta
import joblib
import io
import calendar

CACHE_DURATION = timedelta(hours=24)

@st.cache_resource(ttl=CACHE_DURATION, show_spinner=True, max_entries=10)
def load_eda_data():
    URL = st.secrets["EDA_DATA_URL"]
    response = requests.get(URL).content
    df = pd.read_csv(BytesIO(response))

    df = df.rename(columns={
        "mean_temp_2m": "Mean Temperature",
        "humidity_2m": "Humidity",
        "total_rain": "Rainfall",
        "enso_status": "ENSO"
    })

    return df

def dataset_info(df):
    df_1 = df.drop(columns=["Unnamed: 0"], errors="ignore")
    summary = pd.DataFrame([{
        "Column": col,
        "Count": df_1[col].count(),
        "Type": df_1[col].dtype
    } for col in df_1.columns])

    summary["Type"] = summary["Type"].astype(str)
    return summary

def enso_status_decoder(oni_index):
    if oni_index == 0:
        return "Neutral"
    elif oni_index == 1:
        return "Weak La Niña"
    elif oni_index == 2:
        return "Moderate La Niña"
    elif oni_index == 3:
        return "Strong La Niña"
    elif oni_index == 4:
        return "Very Strong La Niña"
    elif oni_index == 5:
        return "Weak El Niño"
    elif oni_index == 6:
        return "Moderate El Niño"
    elif oni_index == 7:
        return "Strong El Niño"
    elif oni_index == 8:
        return "Very Strong El Niño"
    else:
        return "Unknown"

@st.cache_resource(ttl=CACHE_DURATION, show_spinner=True, max_entries=10)
def parse_model():
    MODEL_URL = st.secrets["MODEL_URL"]
    resp = requests.get(MODEL_URL)
    resp.raise_for_status()
    content = resp.content 
    artifacts = joblib.load(io.BytesIO(content))
    pipeline = artifacts.get("pipeline")
    encoder = artifacts.get("encoder")
    return encoder, pipeline

def make_predictions(payload):

    encoder, pipeline = parse_model()

    X_base = pd.DataFrame([payload])

    X_encoded = encoder.transform(X_base)
    prediction = pipeline.predict(X_encoded)[0]

    # Consolidations
    labels = {0: "Normal", 1: "Elevated", 2: "Outbreak"}
    current_month = int(payload.get("Month"))
    lead_months = 3
    forecast_month = (current_month + lead_months - 1) % 12 + 1
    forecast_month_name = calendar.month_name[forecast_month]

    result = {
        "month_ahead": lead_months,
        "target_month": forecast_month_name,
        "predicted_outbreak_level": int(prediction),
        "risk_category": labels.get(int(prediction))
    }

    return result