# ============================================================
# 🧩 FINAL FEATURE ENRICHMENT PIPELINE (LOCAL EXECUTION)
# ============================================================

import os, re, io, cv2, requests, emoji, ftfy, textstat
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer
from langdetect import detect, DetectorFactory

# ============================================================
# CONFIGURATION
# ============================================================
DetectorFactory.seed = 0
tqdm.pandas()
MAIN_PATH = r"M:\Documents\Projects\ViewTrendsSL\data\upload\merged_with_channel_data_updated.csv"
OUTPUT_PATH = MAIN_PATH.replace("_updated.csv", "_final.csv")

# ============================================================
# 1️⃣ LOAD DATASET
# ============================================================
df = pd.read_csv(MAIN_PATH)
print(f"✅ Loaded main dataset: {df.shape[0]} videos")

# ============================================================
# 2️⃣ TEXTUAL FEATURES (title_pca2, desc150_pca2)
# ============================================================

def clean_text(text):
    if pd.isna(text): return ""
    text = ftfy.fix_text(str(text))
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'#[A-Za-z0-9_]+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^\w\s\u0D80-\u0DFF\u0B80-\u0BFF]', '', text)
    return text.strip().lower()

print("🧹 Cleaning text fields...")
df['title_clean'] = df['title'].apply(clean_text)
df['desc150'] = df['description'].astype(str).str[:150].apply(clean_text)

print("🔄 Loading multilingual model...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

print("🔍 Encoding text embeddings (this may take 3–5 min)...")
emb_title = model.encode(df['title_clean'].tolist(), show_progress_bar=True, batch_size=64)
emb_desc150 = model.encode(df['desc150'].tolist(), show_progress_bar=True, batch_size=64)

def embed_to_pca(emb, prefix):
    scaler = StandardScaler()
    emb_scaled = scaler.fit_transform(emb)
    pca = PCA(n_components=5, random_state=42)
    reduced = pca.fit_transform(emb_scaled)
    print(f"🧩 {prefix}: {round(pca.explained_variance_ratio_.sum()*100,2)}% variance retained")
    df_pca = pd.DataFrame(reduced, columns=[f"{prefix}_pca{i+1}" for i in range(5)])
    return df_pca

pca_title_df = embed_to_pca(emb_title, "title")
pca_desc150_df = embed_to_pca(emb_desc150, "desc150")

df_text = pd.concat([df[['id']], pca_title_df[['title_pca2']], pca_desc150_df[['desc150_pca2']]], axis=1)
print("✅ Text features created.")

# ============================================================
# 3️⃣ VISUAL FEATURES (sharpness, colorfulness)
# ============================================================

def load_image(url):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return np.array(Image.open(io.BytesIO(resp.content)).convert("RGB"))
    except Exception:
        return None
    return None

def extract_visual_features(img):
    if img is None:
        return dict(sharpness=np.nan, colorfulness=np.nan)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    (B, G, R) = cv2.split(img.astype("float"))
    rg = np.abs(R - G)
    yb = np.abs(0.5*(R + G) - B)
    colorfulness = np.sqrt(np.mean(rg**2) + np.mean(yb**2))
    return dict(sharpness=sharpness, colorfulness=colorfulness)

print("🖼️ Extracting sharpness & colorfulness for all videos...")
visual_results = []
for _, row in tqdm(df.iterrows(), total=len(df)):
    thumb_url = row.get('thumbnail_high')
    if pd.isna(thumb_url):
        visual_results.append({'sharpness': np.nan, 'colorfulness': np.nan})
        continue
    img = load_image(thumb_url)
    feats = extract_visual_features(img)
    visual_results.append(feats)

df_visual = pd.DataFrame(visual_results)
df_visual['id'] = df['id']
print("✅ Visual features created.")

# ============================================================
# 4️⃣ MERGE FEATURES
# ============================================================
df_final = df.merge(df_text, on='id', how='left').merge(df_visual, on='id', how='left')
print(f"✅ Merged dataset: {df_final.shape}")

# ============================================================
# 5️⃣ REMOVE INTERMEDIATE TEXT & THUMBNAIL COLUMNS
# ============================================================
drop_cols = [c for c in df_final.columns if any(k in c.lower() for k in [
    'thumbnail_', 'localized_', 'tags', 'title_clean', 'desc150', 'default_language',
    'default_audio_language', 'live_broadcast_content'
])]
df_final = df_final.drop(columns=drop_cols, errors='ignore')

# keep only the derived text & visual features
keep_core = ['id', 'published_at', 'channel_id', 'category_id',
             'video_duration', 'video_width', 'video_height', 'video_orientation',
             'video_fps', 'video_bitrate',
             'view_count', 'likes_count', 'comment_count',
             'channel_subs', 'channel_total_views', 'channel_no_of_videos',
             'title_pca2', 'desc150_pca2', 'sharpness', 'colorfulness']

# keep also all temporal day_X columns if they exist
temporal_cols = [c for c in df_final.columns if c.startswith("day_")]
df_final = df_final[[c for c in keep_core if c in df_final.columns] + temporal_cols]

print("🧹 Cleaned dataset to final schema.")

# ============================================================
# 6️⃣ SAVE RESULTS
# ============================================================
df_final.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Final dataset saved to: {OUTPUT_PATH}")