def daily_efficiency_envelope(df):
    return {
        "Best (90th pct)": round(df["boiler_efficiency_pct"].quantile(0.9), 2),
        "Typical (Median)": round(df["boiler_efficiency_pct"].median(), 2),
        "Worst (10th pct)": round(df["boiler_efficiency_pct"].quantile(0.1), 2)
    }
