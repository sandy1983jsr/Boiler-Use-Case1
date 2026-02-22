import pandas as pd
from digital_twin.boiler_physics import boiler_efficiency_asme

def run_digital_twin(df, fuel_gcv):
    efficiencies = []

    for _, row in df.iterrows():
        eff = boiler_efficiency_asme(
            fuel_gcv_kcal_per_kg=fuel_gcv,
            fuel_flow_kgph=row["fuel_kgph"],
            steam_flow_kgph=row["steam_tph"] * 1000,
            flue_gas_temp_c=row["stack_temp_c"],
            o2_pct=row["o2_pct"],
            co_ppm=row["co_ppm"]
        )
        efficiencies.append(eff)

    df["boiler_efficiency_pct"] = efficiencies
    return df
