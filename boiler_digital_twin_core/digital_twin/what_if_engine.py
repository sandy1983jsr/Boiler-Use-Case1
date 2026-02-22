# digital_twin/what_if_engine.py

from digital_twin.boiler_physics import boiler_efficiency_asme

def run_what_if(
    base_row,
    fuel_gcv,
    new_o2=None,
    new_stack_temp=None,
    new_load=None
):
    """
    Physics-consistent what-if:
    SAME steam demand, recalculated fuel requirement
    """

    # --- Base values ---
    base_o2 = base_row["o2_pct"]
    base_stack = base_row["stack_temp_c"]
    base_steam_tph = base_row["steam_tph"]
    base_fuel_kgph = base_row["fuel_kgph"]

    # --- Apply what-if changes ---
    o2 = new_o2 if new_o2 is not None else base_o2
    stack_temp = new_stack_temp if new_stack_temp is not None else base_stack

    if new_load is None:
        steam_tph = base_steam_tph
    else:
        steam_tph = base_steam_tph * (new_load / base_row["load_pct"])

    # --- Step 1: Calculate useful heat (fixed demand) ---
    steam_enthalpy = 660      # kcal/kg
    feedwater_enthalpy = 105  # kcal/kg

    useful_heat = steam_tph * 1000 * (steam_enthalpy - feedwater_enthalpy)

    # --- Step 2: Estimate losses under new conditions ---
    excess_air_ratio = 21 / (21 - o2)

    dry_flue_loss = 0.01 * (stack_temp - 30) * excess_air_ratio
    combustion_loss = 0.0001 * base_row["co_ppm"]
    radiation_loss = 1.5

    total_loss_pct = dry_flue_loss + combustion_loss + radiation_loss

    # --- Step 3: Back-calculate required fuel ---
    required_fuel = useful_heat / (
        fuel_gcv * (1 - total_loss_pct / 100)
    )

    # --- Step 4: Recompute efficiency ---
    efficiency = (useful_heat / (required_fuel * fuel_gcv)) * 100

    return round(efficiency, 2)
