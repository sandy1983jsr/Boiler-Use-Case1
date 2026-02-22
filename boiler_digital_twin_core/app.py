import streamlit as st
import pandas as pd
from digital_twin.efficiency_engine import run_digital_twin

st.set_page_config("Boiler Digital Twin – Engineering", layout="wide")

st.title("Briquette Boiler Digital Twin (Physics-Based)")

# Load data
uploaded = st.file_uploader("Upload boiler CSV (or use demo)", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/demo_boiler_data.csv")

fuel_gcv = st.number_input(
    "Fuel GCV (kcal/kg)", min_value=3000, max_value=4200, value=3800
)

df = run_digital_twin(df, fuel_gcv)

st.subheader("Boiler Efficiency Trend (%)")
st.line_chart(df.set_index("timestamp")["boiler_efficiency_pct"])

st.subheader("Underlying Data")
st.dataframe(df)
