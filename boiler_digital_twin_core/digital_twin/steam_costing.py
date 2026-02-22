def cost_per_ton_steam(
    fuel_cost_rs_per_kg,
    fuel_kgph,
    steam_tph
):
    if steam_tph == 0:
        return None
    return round((fuel_kgph * fuel_cost_rs_per_kg) / steam_tph, 2)
