def boiler_efficiency_asme(
    fuel_gcv_kcal_per_kg,
    fuel_flow_kgph,
    steam_flow_kgph,
    steam_enthalpy_kcal_per_kg=660,
    feedwater_enthalpy_kcal_per_kg=105,
    flue_gas_temp_c=200,
    ambient_temp_c=30,
    o2_pct=6.0,
    co_ppm=200
):
    """
    ASME heat-loss method (simplified for briquette / biomass boilers)
    ALWAYS returns a dictionary
    """

    # Useful heat
    useful_heat = steam_flow_kgph * (
        steam_enthalpy_kcal_per_kg - feedwater_enthalpy_kcal_per_kg
    )

    # Heat input
    heat_input = fuel_flow_kgph * fuel_gcv_kcal_per_kg

    # Excess air ratio
    excess_air_ratio = 21 / (21 - o2_pct)

    # Losses (%)
    dry_flue_gas_loss = 0.01 * (flue_gas_temp_c - ambient_temp_c) * excess_air_ratio
    incomplete_combustion_loss = 0.0001 * co_ppm
    radiation_loss = 1.5  # typical biomass boiler

    efficiency_pct = (useful_heat / heat_input) * 100

    return {
        "efficiency_pct": round(efficiency_pct, 2),
        "losses": {
            "Dry flue gas loss (%)": round(dry_flue_gas_loss, 2),
            "Incomplete combustion loss (%)": round(incomplete_combustion_loss, 2),
            "Radiation & others (%)": radiation_loss
        }
    }
