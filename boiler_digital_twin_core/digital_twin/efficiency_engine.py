import pandas as pd
from digital_twin.boiler_physics import boiler_efficiency_asme

def run_digital_twin(df, fuel_gcv):
    results = []

    for _, r in df.iterrows():
        res = boiler_efficiency_asme(
            fuel_gcv_kcal_per_kg=fuel_gcv,
            fuel_flow_kgph=r["fuel_kgph"],
            steam_flow_kgph=r["steam_tph"] * 1000,
            flue_gas_temp_c=r["stack_temp_c"],
            o2_pct=r["o2_pct"],
            co_ppm=r["co_ppm"]
        )
        results.append(res["boiler_efficiency_pct"])

    df["boiler_efficiency_pct"] = results
    return df
