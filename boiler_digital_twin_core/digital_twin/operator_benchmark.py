def assign_shift(hour):
    if 6 <= hour < 14:
        return "Shift A"
    elif 14 <= hour < 22:
        return "Shift B"
    else:
        return "Shift C"

def operator_efficiency(df):
    df["shift"] = df["timestamp"].dt.hour.apply(assign_shift)
    return (
        df.groupby("shift")["boiler_efficiency_pct"]
        .mean()
        .round(2)
        .reset_index()
    )
