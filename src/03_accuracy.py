import pandas as pd

# ── Load data ──────────────────────────────────────────
print("Loading data...")
targets = pd.read_parquet("data/processed/ptgdet_clean.parquet")
prices  = pd.read_parquet("data/prices/prices.parquet")

# ── Step 1: Keep matched tickers only ─────────────────
price_tickers = set(prices["ticker"].unique())
targets = targets[targets["OFTIC"].isin(price_tickers)].copy()

# ── Step 2: Sort + fix datetime precision ──────────────
targets = targets.sort_values("ANNDATS").reset_index(drop=True)
prices  = prices.sort_values("Date").reset_index(drop=True)
targets["ANNDATS"] = targets["ANNDATS"].astype("datetime64[ms]")
prices["Date"]     = prices["Date"].astype("datetime64[ms]")

# ── Step 3: Join T=0 price ─────────────────────────────
print("Joining T=0 prices...")
prices_t0 = prices.rename(columns={"ticker": "OFTIC",
                                    "Date": "ANNDATS",
                                    "adj_close": "price_t0"})
df = pd.merge_asof(targets, prices_t0,
                   on="ANNDATS", by="OFTIC",
                   direction="nearest",
                   tolerance=pd.Timedelta("5 days"))
df = df.dropna(subset=["price_t0"])

# ── Step 4: Outlier filter + implied upside ────────────
df = df[df["VALUE"] > 0]
df = df[df["price_t0"] >= 1]
df["implied_upside"] = (df["VALUE"] - df["price_t0"]) / df["price_t0"]
df = df[df["implied_upside"].between(-1, 5)].copy()
print(f"  Rows after T=0 join: {len(df):,}")

# ── Step 5: Build T+365 date column ───────────────────
print("Joining T+365 prices...")
df["date_t365"] = df["ANNDATS"] + pd.Timedelta(days=365)

# Only keep rows where T+365 is before end of price data
max_price_date = prices["Date"].max()
df = df[df["date_t365"] <= max_price_date].copy()
print(f"  Rows with T+365 in range: {len(df):,}")

# ── Step 6: Join T+365 price ───────────────────────────
prices_t365 = prices.rename(columns={"ticker":    "OFTIC",
                                      "Date":      "date_t365",
                                      "adj_close": "price_t365"})
df["date_t365"]              = df["date_t365"].astype("datetime64[ms]")
prices_t365["date_t365"]     = prices_t365["date_t365"].astype("datetime64[ms]")

prices_t365 = prices_t365.sort_values("date_t365").reset_index(drop=True)
df          = df.sort_values("date_t365").reset_index(drop=True)

df = pd.merge_asof(df, prices_t365,
                   on="date_t365", by="OFTIC",
                   direction="nearest",
                   tolerance=pd.Timedelta("5 days"))
df = df.dropna(subset=["price_t365"])
print(f"  Rows with T+365 price: {len(df):,}")

# ── Step 7: Compute accuracy metrics ──────────────────
print("Computing accuracy metrics...")
df["actual_return"] = (df["price_t365"] - df["price_t0"]) / df["price_t0"]
df["error"]         = df["implied_upside"] - df["actual_return"]
df["abs_error"]     = df["error"].abs()
df["directional_hit"] = (
    (df["implied_upside"] > 0) == (df["actual_return"] > 0)
).astype(int)

# ── Step 8: Save ───────────────────────────────────────
out = "data/processed/accuracy.parquet"
df.to_parquet(out, index=False)
print(f"\nSaved: {out}")
print(f"Final shape: {df.shape}")

print("\nAccuracy metric stats:")
print(df[["implied_upside","actual_return",
          "error","abs_error","directional_hit"]].describe().round(3))