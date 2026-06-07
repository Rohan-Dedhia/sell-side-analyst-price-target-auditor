import pandas as pd
import yfinance as yf
import os
import time
from tqdm import tqdm

# ── Config ─────────────────────────────────────────────
TOP_N      = 1000          # only download top N most-covered tickers
BATCH_SIZE = 50            # tickers per yfinance request
SLEEP_SEC  = 2             # pause between batches (avoid rate limits)
START_DATE = "2001-01-01"
END_DATE   = "2025-03-01"
PRICES_DIR = "data/prices"

os.makedirs(PRICES_DIR, exist_ok=True)

# ── Step 1: Get top N tickers ──────────────────────────
print("Loading cleaned data...")
df = pd.read_parquet("data/processed/ptgdet_clean.parquet")

coverage  = df.groupby("OFTIC").size().sort_values(ascending=False)
top_tickers = coverage.head(TOP_N).index.tolist()

print(f"  Top {TOP_N} tickers selected")
print(f"  These cover {df[df['OFTIC'].isin(top_tickers)].shape[0]:,} of {len(df):,} rows")
print(f"  Date range to download: {START_DATE} to {END_DATE}\n")

# ── Step 2: Split into batches ─────────────────────────
batches = [top_tickers[i:i+BATCH_SIZE] 
           for i in range(0, len(top_tickers), BATCH_SIZE)]
print(f"  {len(batches)} batches of {BATCH_SIZE} tickers each\n")

# ── Step 3: Download batch by batch ───────────────────
all_prices = []
failed_batches = []

for i, batch in enumerate(tqdm(batches, desc="Downloading prices")):
    try:
        raw = yf.download(
            tickers    = batch,
            start      = START_DATE,
            end        = END_DATE,
            auto_adjust= True,
            progress   = False,
        )

        # extract adjusted close only
        if len(batch) == 1:
            close = raw[["Close"]].copy()
            close.columns = [batch[0]]
        else:
            close = raw["Close"]

        # reshape to long format: date, ticker, adj_close
        close = close.reset_index().melt(
            id_vars   = "Date",
            var_name  = "ticker",
            value_name= "adj_close"
        )
        close = close.dropna(subset=["adj_close"])
        all_prices.append(close)

    except Exception as e:
        print(f"\n  Batch {i} failed: {e}")
        failed_batches.append(batch)

    time.sleep(SLEEP_SEC)

# ── Step 4: Combine and save ───────────────────────────
print("\nCombining all batches...")
prices = pd.concat(all_prices, ignore_index=True)
prices["Date"] = pd.to_datetime(prices["Date"])
prices = prices.sort_values(["ticker", "Date"]).reset_index(drop=True)

out_path = f"{PRICES_DIR}/prices.parquet"
prices.to_parquet(out_path, index=False)

print(f"  Saved: {out_path}")
print(f"  Shape: {prices.shape}")
print(f"  Tickers downloaded: {prices['ticker'].nunique():,}")
print(f"  Date range: {prices['Date'].min().date()} to {prices['Date'].max().date()}")

if failed_batches:
    flat = [t for b in failed_batches for t in b]
    print(f"\n  WARNING: {len(flat)} tickers failed — rerun script to retry")