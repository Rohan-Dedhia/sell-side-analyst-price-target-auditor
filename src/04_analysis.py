import pandas as pd

# ── Load ───────────────────────────────────────────────
print("Loading accuracy data...")
df = pd.read_parquet("data/processed/accuracy.parquet")
print(f"  {len(df):,} graded forecasts")

# ── Firm-level accuracy ranking ────────────────────────
firm = df.groupby("firm_name").agg(
    total_targets    = ("error",           "count"),
    mean_bias        = ("error",           "mean"),
    mean_abs_error   = ("abs_error",       "mean"),
    directional_acc  = ("directional_hit", "mean"),
    mean_actual_ret  = ("actual_return",   "mean"),
    mean_implied_up  = ("implied_upside",  "mean"),
).round(3)

# Keep only firms with meaningful sample size
firm = firm[firm["total_targets"] >= 100].copy()
firm = firm.sort_values("mean_bias", ascending=False)

# Convert to percentages for readability
for col in ["mean_bias","mean_abs_error","directional_acc",
            "mean_actual_ret","mean_implied_up"]:
    firm[col] = (firm[col] * 100).round(1)

firm.columns = ["Targets","Bias(pp)","MAE(pp)",
                "Dir.Acc(%)","Actual Ret(%)","Implied Up(%)"]

print("\nFirm-level accuracy ranking (sorted by bias — most bullish first):")
print(firm.to_string())

# ── Market regime analysis ─────────────────────────────
df["year"] = df["ANNDATS"].dt.year

regime_map = {
    range(2001, 2003): "Dot-com bust (2001-02)",
    range(2003, 2008): "Bull market (2003-07)",
    range(2008, 2010): "GFC (2008-09)",
    range(2010, 2022): "Bull market (2010-21)",
    range(2022, 2023): "Bear market (2022)",
    range(2023, 2026): "Recovery (2023-24)",
}

def assign_regime(year):
    for r, label in regime_map.items():
        if year in r:
            return label
    return "Other"

df["regime"] = df["year"].apply(assign_regime)

regime = df.groupby("regime").agg(
    targets         = ("error",           "count"),
    mean_bias       = ("error",           "mean"),
    directional_acc = ("directional_hit", "mean"),
    mean_actual_ret = ("actual_return",   "mean"),
).round(3)

for col in ["mean_bias","directional_acc","mean_actual_ret"]:
    regime[col] = (regime[col] * 100).round(1)

regime.columns = ["Targets","Bias(pp)","Dir.Acc(%)","Actual Ret(%)"]
regime = regime.sort_values("Bias(pp)", ascending=False)

print("\nBias by market regime:")
print(regime.to_string())

# ── Save all results ───────────────────────────────────
import os
os.makedirs("outputs", exist_ok=True)
firm.to_csv("outputs/firm_accuracy.csv")
regime.to_csv("outputs/regime_accuracy.csv")
print("\nSaved: outputs/firm_accuracy.csv")
print("Saved: outputs/regime_accuracy.csv")

# ── Year-by-year bias trend ────────────────────────────
yearly = df.groupby("year").agg(
    targets         = ("error",           "count"),
    mean_bias       = ("error",           "mean"),
    directional_acc = ("directional_hit", "mean"),
    mean_actual_ret = ("actual_return",   "mean"),
).round(3)

for col in ["mean_bias","directional_acc","mean_actual_ret"]:
    yearly[col] = (yearly[col] * 100).round(1)

yearly.columns = ["Targets","Bias(pp)","Dir.Acc(%)","Actual Ret(%)"]
print("\nYear-by-year bias trend:")
print(yearly.to_string())

# ── Three analyst leaderboards ─────────────────────────
analyst = df.groupby(["ALYSNAM","firm_name"]).agg(
    targets         = ("error",           "count"),
    mean_bias       = ("error",           "mean"),
    mean_abs_error  = ("abs_error",       "mean"),
    directional_acc = ("directional_hit", "mean"),
).round(3)

analyst = analyst[analyst["targets"] >= 50].copy()

for col in ["mean_bias","mean_abs_error","directional_acc"]:
    analyst[col] = (analyst[col] * 100).round(1)

analyst.columns = ["Targets","Bias(pp)","MAE(pp)","Dir.Acc(%)"]

qualified = analyst[analyst["Targets"] >= 100].copy()

print("\nLeaderboard 1 — Most Accurate (lowest MAE):")
print(qualified.sort_values("MAE(pp)").head(20).to_string())

print("\nLeaderboard 2 — Most Calibrated (bias closest to zero):")
qualified["abs_bias"] = qualified["Bias(pp)"].abs()
print(qualified.sort_values("abs_bias")
      .drop(columns="abs_bias").head(20).to_string())

print("\nLeaderboard 3 — Best Direction Predictors:")
print(qualified.sort_values("Dir.Acc(%)", ascending=False).head(20).to_string())

print("\nLeaderboard 4 — Most Bullish (for reference):")
print(qualified.sort_values("Bias(pp)", ascending=False).head(20).to_string())

# ── Save ───────────────────────────────────────────────
yearly.to_csv("outputs/yearly_accuracy.csv")
analyst.to_csv("outputs/analyst_accuracy.csv")
print("\nSaved: outputs/yearly_accuracy.csv")
print("Saved: outputs/analyst_accuracy.csv")