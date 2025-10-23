import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# === Config ===
CSV_PATH = r"M:\Documents\Projects\ViewTrendsSL\data\upload\merged_with_channel_data_without_thumbnail_data.csv"
OUTPUT_PATH = CSV_PATH.replace(".csv")
MAX_WORKERS = 20  # Adjust based on your internet speed
TIMEOUT = 10

print("📂 Loading dataset...")
df = pd.read_csv(CSV_PATH)

# === Helper to fetch width/height ===
def fetch_resolution(url):
    if pd.isna(url) or not isinstance(url, str) or 'ytimg.com' not in url:
        return (None, None)
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
        return img.size  # (width, height)
    except Exception:
        return (None, None)

# === Parallel download ===
urls = df['thumbnail_default'].dropna().unique()
print(f"🖼️ Fetching resolutions for {len(urls):,} unique thumbnail_default URLs...")

resolution_map = {}
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_url = {executor.submit(fetch_resolution, u): u for u in urls}
    for i, future in enumerate(as_completed(future_to_url), 1):
        url = future_to_url[future]
        width, height = future.result()
        resolution_map[url] = (width, height)
        if i % 500 == 0:
            print(f"  ⏳ Processed {i:,}/{len(urls):,} thumbnails...")

print("✅ Fetch complete! Attaching resolutions to DataFrame...")

# === Attach to main dataframe ===
df['thumb_width'] = df['thumbnail_default'].map(lambda u: resolution_map.get(u, (None, None))[0])
df['thumb_height'] = df['thumbnail_default'].map(lambda u: resolution_map.get(u, (None, None))[1])

# === Compute derived features ===
df['thumb_resolution'] = df.apply(
    lambda x: f"{int(x.thumb_width)}x{int(x.thumb_height)}" if pd.notna(x.thumb_width) and pd.notna(x.thumb_height) else None,
    axis=1
)

def classify_orientation(w, h):
    if pd.isna(w) or pd.isna(h):
        return "unknown"
    ratio = w / h
    if 0.9 <= ratio <= 1.1:
        return "square"
    elif ratio < 0.9:
        return "portrait"
    else:
        return "landscape"

df['thumb_orientation'] = df.apply(lambda x: classify_orientation(x.thumb_width, x.thumb_height), axis=1)

# === Save ===
df.to_csv(OUTPUT_PATH, index=False)
print(f"💾 Saved updated file with thumbnail metadata → {OUTPUT_PATH}")
