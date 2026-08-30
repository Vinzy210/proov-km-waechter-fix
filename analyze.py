# analyze.py
# Breakdown-risk analysis for Vossberg Mobility fleet.
#
# Key findings (from fleet_history.csv, 120 cars, 26 breakdowns):
#   - avg_daily_km and load_factor are the strongest predictors of breakdown.
#     Cars that broke down averaged 160 km/day vs 131 for cars that did not,
#     and 0.60 load vs 0.50.
#   - Total odometer_km and age_years show almost NO difference between groups
#     (53,448 km vs 53,302 km; age identical at 5.9 years) — the "older/
#     higher-mileage cars break more" assumption is NOT supported by this data.
#   - km_since_service shows a moderate signal (11,678 vs 7,261 km): cars
#     further into their current service window break down more often.
#
# Risk score (0–100): weighted sum of the three signals that actually separate
# the groups, normalised to the observed range in this dataset.

import pandas as pd

# ── 1. Load data ─────────────────────────────────────────────────────────────
df = pd.read_csv("fleet_history.csv")

# ── 2. Compare groups column by column ───────────────────────────────────────
print("=== Mean values by breakdown status ===")
print(df.groupby("broke_down")[
    ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
].mean().round(1).to_string())
print()

# ── 3. Build risk score from the three separating factors ────────────────────
#
# Normalise each signal to [0, 1] using the column's observed min/max, then
# weight them by how cleanly they separate the two groups.
#   avg_daily_km  → weight 0.40  (biggest group mean difference)
#   load_factor   → weight 0.35  (second-strongest signal)
#   km_since_service → weight 0.25  (moderate signal)

def normalise(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.0, index=series.index)
    return (series - lo) / (hi - lo)

df["risk_score"] = (
    0.40 * normalise(df["avg_daily_km"])
    + 0.35 * normalise(df["load_factor"])
    + 0.25 * normalise(df["km_since_service"])
) * 100

# ── 4. Print cars ranked by risk, highest first ───────────────────────────────
ranked = df[["car_id", "risk_score", "avg_daily_km", "load_factor",
             "km_since_service", "broke_down"]].sort_values(
    "risk_score", ascending=False
).reset_index(drop=True)

ranked["risk_score"] = ranked["risk_score"].round(1)

print("=== Fleet ranked by breakdown risk (highest first) ===")
print(ranked.to_string(index=False))
print()

# ── 5. Quick accuracy check: do the top-risk cars overlap with actual breakdowns? ─
n_broke = df["broke_down"].sum()
top_n = ranked.head(n_broke)
overlap = top_n["broke_down"].sum()
print(f"Cars that actually broke down: {n_broke}")
print(f"Of the top-{n_broke} highest-risk cars, {overlap} did break down "
      f"({100 * overlap / n_broke:.0f}% recall).")
