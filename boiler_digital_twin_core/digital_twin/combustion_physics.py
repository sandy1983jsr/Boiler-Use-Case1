def excess_air_ratio(o2_pct):
    return 21 / (21 - o2_pct)

def recommended_o2_range(load_pct):
    if load_pct >= 80:
        return (4.5, 6.0)
    elif load_pct >= 60:
        return (5.5, 7.0)
    else:
        return (6.5, 8.5)
