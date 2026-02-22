from digital_twin.boiler_physics import boiler_efficiency_asme

def run_what_if(
    base_row,
    fuel_gcv,
    new_o2=None,
    new_stack_temp=None,
    new_load=None
):
    o2 = new_o2 if new_o2 is not None else base_row["o2_pct"]
    stack_temp = (
        new_stack_temp if new_stack_temp is not None else base_row["stack_temp_c"]
    )

    if new_load is None:
        steam_tph = base_row["steam_tph"]
    else:
        steam_tph = base_row["steam_tph"] * (new_load / base_row["load_pct"])

    result = boiler_efficiency_asme(
        fuel_gcv_kcal_per_kg=fuel_gcv,
        fuel_flow_kgph=base_row["fuel_kgph"],
        steam_flow_kgph=steam_tph * 1000,
        flue_gas_temp_c=stack_temp,
        o2_pct=o2,
        co_ppm=base_row["co_ppm"]
    )

    return result["efficiency_pct"]
