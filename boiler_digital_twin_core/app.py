import sys
import os
import streamlit as st
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from digital_twin.efficiency_engine import run_digital_twin
from digital_twin.what_if_engine import run_what_if
from digital_twin.o2_recommendation import recommend_o2_band
from digital_twin.efficiency_envelope import daily_efficiency_envelope
from digital_twin.steam_costing import cost_per_ton_steam
from digital_twin.operator_benchmark import operator_efficiency

st.set_page_config("Boiler Digital Twin", layout="wide")
st.title("🔥 Briquette Boiler Digital Twin – Decision Support")

# ---------------- Data ----------------
uploaded = st.file_uploader("Upload boiler CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "demo_boiler_data.csv"))

df["timestamp"] = pd.to_datetime(df["timestamp"])

fuel_gcv = st.number_input("Fuel GCV (kcal/kg)", 3000, 4200, 3800, 50)
fuel_cost = st.number_input("Fuel Cost (₹/kg)", 2.0, 12.0, 6.5, 0.5)

df = run_digital_twin(df, fuel_gcv)

# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Performance",
    "🔍 Diagnostics",
    "🔮 What-If",
    "👷 Operator Benchmark"
])

# ===== TAB 1: PERFORMANCE =====
with tab1:
    st.subheader("Boiler Efficiency Trend (%)")
    st.line_chart(df.set_index("timestamp")["boiler_efficiency_pct"])

    envelope = daily_efficiency_envelope(df)
    st.write("### Daily Efficiency Envelope")
    st.json(envelope)

    latest = df.iloc[-1]
    steam_cost = cost_per_ton_steam(
        fuel_cost,
        latest["fuel_kgph"],
        latest["steam_tph"]
    )
    st.metric("₹ / ton steam", steam_cost)

# ===== TAB 2: DIAGNOSTICS =====
with tab2:
    st.subheader("Efficiency Drivers")
    st.line_chart(
        df.set_index("timestamp")[[
            "boiler_efficiency_pct",
            "flue_gas_loss_pct",
            "combustion_loss_pct"
        ]]
    )

    o2_min, o2_max = recommend_o2_band(df, latest["load_pct"])
    st.success(f"✅ AI-recommended O₂ band: **{o2_min}% – {o2_max}%**")

# ===== TAB 3: WHAT-IF =====
with tab3:
    st.subheader("What-If Scenario")

    new_o2 = st.slider("O₂ (%)", 4.0, 9.0, float(latest["o2_pct"]), 0.1)
    new_stack = st.slider("Stack Temp (°C)", 160, 260, int(latest["stack_temp_c"]), 5)
    new_load = st.slider("Load (%)", 50, 100, int(latest["load_pct"]), 5)

    pred_eff = run_what_if(
        latest,
        fuel_gcv,
        new_o2=new_o2,
        new_stack_temp=new_stack,
        new_load=new_load
    )

    st.metric(
        "Predicted Boiler Efficiency (%)",
        pred_eff,
        round(pred_eff - latest["boiler_efficiency_pct"], 2)
    )

# ===== TAB 4: OPERATOR =====
with tab4:
    st.subheader("Shift-wise Boiler Efficiency")
    op = operator_efficiency(df)
    st.bar_chart(op.set_index("shift"))
