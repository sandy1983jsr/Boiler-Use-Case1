from digital_twin.boiler_physics import boiler_efficiency_asme

def run_digital_twin(df, fuel_gcv):
    eff_list = []
    flue_loss_list = []
    combustion_loss_list = []

    for _, r in df.iterrows():
        result = boiler_efficiency_asme(
            fuel_gcv_kcal_per_kg=fuel_gcv,
            fuel_flow_kgph=r["fuel_kgph"],
            steam_flow_kgph=r["steam_tph"] * 1000,
            flue_gas_temp_c=r["stack_temp_c"],
            o2_pct=r["o2_pct"],
            co_ppm=r["co_ppm"]
        )

        eff_list.append(result["efficiency_pct"])
        flue_loss_list.append(result["losses"]["Dry flue gas loss (%)"])
        combustion_loss_list.append(result["losses"]["Incomplete combustion loss (%)"])

    df["boiler_efficiency_pct"] = eff_list
    df["flue_gas_loss_pct"] = flue_loss_list
    df["combustion_loss_pct"] = combustion_loss_list

    return df
