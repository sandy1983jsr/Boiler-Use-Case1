import numpy as np

def recommend_o2_band(df, load_pct):
    """
    Data-driven O2 band constrained by combustion physics
    """

    # Physics guardrails
    if load_pct >= 80:
        phys_min, phys_max = 4.5, 6.0
    elif load_pct >= 60:
        phys_min, phys_max = 5.5, 7.0
    else:
        phys_min, phys_max = 6.5, 8.5

    # Data-driven optimal zone (highest efficiency quartile)
    top_eff = df[df["boiler_efficiency_pct"] >= df["boiler_efficiency_pct"].quantile(0.75)]
    data_min = top_eff["o2_pct"].quantile(0.25)
    data_max = top_eff["o2_pct"].quantile(0.75)

    # Final recommendation (intersection)
    rec_min = max(phys_min, data_min)
    rec_max = min(phys_max, data_max)

    return round(rec_min, 2), round(rec_max, 2)
