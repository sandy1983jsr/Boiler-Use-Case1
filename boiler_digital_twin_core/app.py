import sys
import os
import streamlit as st
import pandas as pd

# --- Fix paths for Streamlit Cloud ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from digital_twin.efficiency_engine import run_digital_twin

st.set_page_config(
    page_title="Briquette Boiler Digital Twin",
    layout="wide"
)

st.title("🔥 Briquette Boiler Digital Twin (Physics-Based)")
st.caption("ASME heat-loss method | Engineering-grade")

# --- Load data ---
uploaded_file = st.file_uploader(
    "Upload boiler CSV (or use demo data)",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    data_path = os.path.join(BASE_DIR, "data", "demo_boiler_data.csv")
    df = pd.read_csv(data_path)

# --- Parse timestamp safely ---
df["timestamp"] = pd.to_datetime(df["timestamp"])

# --- Fuel input ---
fuel_gcv = st.number_input(
    "Fuel GCV (kcal/kg)",
    min_value=3000,
    max_value=4200,
    value=3800,
    step=50
)

# --- Run digital twin ---
df = run_digital_twin(df, fuel_gcv)

# --- Display results ---
st.subheader("📈 Boiler Efficiency Trend (%)")
st.line_chart(df.set_index("timestamp")["boiler_efficiency_pct"])

st.subheader("📊 Detailed Data")
st.dataframe(df, use_container_width=True)
