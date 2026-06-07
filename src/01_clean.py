import pandas as pd
import os

RAW_PATH       = "data/raw/ptgdet.csv"
PROCESSED_PATH = "data/processed/ptgdet_clean.parquet"

print("Loading raw data...")
df = pd.read_csv(RAW_PATH, low_memory=False)
print(f"  Loaded: {len(df):,} rows")

print("Filtering...")
df = df[df["CURR"]    == "USD"]
df = df[df["HORIZON"] == 12]
df = df[df["USFIRM"]  == 1]
df = df.dropna(subset=["VALUE", "OFTIC", "ANNDATS", "ESTIMID"])
print(f"  After filters: {len(df):,} rows")

print("Cleaning columns...")
df["ANNDATS"]  = pd.to_datetime(df["ANNDATS"])
df["ACTDATS"]  = pd.to_datetime(df["ACTDATS"])
df["ALYSNAM"]  = df["ALYSNAM"].str.strip()
df["OFTIC"]    = df["OFTIC"].str.strip().str.upper()
df["ESTIMID"]  = df["ESTIMID"].str.strip().str.upper()

firm_map = {
    "MERRILL":  "Merrill Lynch / BofA",
    "GOLDMAN":  "Goldman Sachs",
    "JPMORGAN": "JP Morgan",
    "MORGAN":   "Morgan Stanley",
    "JEFFEREG": "Jefferies",
    "FBOSTONM": "FBR Capital Markets",
    "RBCDOMIN": "RBC Capital Markets",
    "FRCLASC":  "Barclays Capital",
    "PIPER":    "Piper Sandler",
    "STIFEL":   "Stifel Nicolaus",
    "RAYMOND":  "Raymond James",
    "KEEFE":    "Keefe Bruyette & Woods",
    "EVERCO":   "Evercore ISI",
    "BERN":     "Bernstein Research",
    "LEHMAN":   "Lehman Brothers",
    "CANACCOR": "Canaccord Genuity",
    "DAVIDSON": "D.A. Davidson",
    "SANDLER":  "Sandler O'Neill",
    "MACQUARI": "Macquarie Securities",
    "WOLFE":    "Wolfe Research",
    "NEEDHAM":  "Needham & Company",
    "SUSQUEH":  "Susquehanna Financial",
    "LAZARD":   "Lazard Capital Markets",
    "NOMURAUS": "Nomura Securities",
    "OPPENM":   "Oppenheimer & Co",
}
df["firm_name"] = df["ESTIMID"].map(firm_map).fillna("Boutique/Other")

print("Saving cleaned file...")
df.to_parquet(PROCESSED_PATH, index=False)
print(f"  Saved to {PROCESSED_PATH}")
print(f"\nDone! Final shape: {df.shape}")
print(df.dtypes)