"""
Phase 2: Feature Engineering + Virality Factor Optimization
-----------------------------------------------------------
Uses:
 - merged_with_channel_data.csv
 - category_leaders.csv

Computes:
 - channel age, video age
 - channel-level performance ratios
 - virality_factor(l,m,n) for grid [-20,20]
 - correlation of virality_factor with day_7_views and day_30_views
 - visualization of optimal l,m,n zones
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from datetime import datetime, timezone

# === Load Data ===
df = pd.read_csv(r"M:\Documents\Projects\ViewTrendsSL\data\raw\merged_with_channel_data.csv")
leaders = pd.read_csv(r"M:\Documents\Projects\ViewTrendsSL\data\raw\cache\category_leaders.csv")

# --- Convert Dates ---
now = datetime.now(timezone.utc)  # UTC-aware datetime

def to_utc(series):
    s = pd.to_datetime(series, errors="coerce", utc=True)
    return s.dt.tz_convert("UTC")

df["published_at"] = to_utc(df["published_at"])
df["created_at"] = to_utc(df["created_at"])
leaders["created_at"] = to_utc(leaders["created_at"])

# Ensure all datetimes are timezone-aware
assert df["created_at"].dt.tz is not None, "created_at still timezone-naive"
assert leaders["created_at"].dt.tz is not None, "leaders.created_at still timezone-naive"

# --- Compute Ages ---
df["video_age_days"] = (now - df["published_at"]).dt.days.clip(lower=1)
df["channel_age_days"] = (now - df["created_at"]).dt.days.clip(lower=1)
leaders["leader_age_days"] = (now - leaders["created_at"]).dt.days.clip(lower=1)

# --- Merge leader stats by category ---
df = df.merge(leaders[["category_id", "subs", "views", "videos", "leader_age_days"]],
              on="category_id", suffixes=("", "_leader"), how="left")

# --- Derived Features ---
df["avg_views_per_video_per_day"] = (df["views"] / (df["videos"] * df["channel_age_days"])).replace([np.inf, np.nan], 0)
df["subs_factor"] = ((df["subs"] + 1) / (df["channel_age_days"] + 1/24)) / ((df["subs_leader"] + 1) / (df["leader_age_days"] + 1/24))
df["views_factor"] = ((df["views"] + 1) / (df["channel_age_days"] + 1/24)) / ((df["views_leader"] + 1) / (df["leader_age_days"] + 1/24))
df["video_factor"] = df["avg_views_per_video_per_day"] / ((df["view_count"] + 1) / (df["video_age_days"] + 1/24))

# Clean up
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

# --- Prepare Outputs ---
corr_results = []
param_grid = range(-20, 21)

print("[INFO] Optimizing l, m, n by correlation with day 7 and 30 views...")

for l in tqdm(param_grid, desc="Testing l exponents"):
    df["vfac_l"] = df["views_factor"] ** l
    for m in param_grid:
        df["sfac_m"] = df["subs_factor"] ** m
        for n in param_grid:
            df["vdfac_n"] = df["video_factor"] ** n
            df["virality_factor"] = -np.log((df["vfac_l"] * df["sfac_m"] * df["vdfac_n"]).clip(lower=1e-9))
            
            corr_7 = df["virality_factor"].corr(df["day_7_views"])
            corr_30 = df["virality_factor"].corr(df["day_30_views"])
            
            corr_results.append({"l": l, "m": m, "n": n, "corr_day7": corr_7, "corr_day30": corr_30})

corr_df = pd.DataFrame(corr_results)
corr_df.to_csv("virality_factor_correlation_grid.csv", index=False)
print("[INFO] Saved grid correlations → virality_factor_correlation_grid.csv")

# --- Find Best Parameters ---
best_7 = corr_df.loc[corr_df["corr_day7"].idxmax()]
best_30 = corr_df.loc[corr_df["corr_day30"].idxmax()]

print("\n=== Optimal Parameters ===")
print(f"Day 7 Views:  l={best_7.l}, m={best_7.m}, n={best_7.n}, corr={best_7.corr_day7:.4f}")
print(f"Day 30 Views: l={best_30.l}, m={best_30.m}, n={best_30.n}, corr={best_30.corr_day30:.4f}")

# --- Visualization ---
plt.figure(figsize=(10, 6))
plt.scatter(corr_df["corr_day7"], corr_df["corr_day30"], s=8, c=corr_df["n"], cmap="coolwarm")
plt.colorbar(label="n exponent")
plt.title("Correlation of Virality Factor with Day 7 vs Day 30 Views")
plt.xlabel("Correlation with Day 7 Views")
plt.ylabel("Correlation with Day 30 Views")
plt.grid(True)
plt.show()
