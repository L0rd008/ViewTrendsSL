===sample initial starting plan(this might subject to change with the information mentioned above)===

## 📌 Project Description – **YouTube Viewership Data Collection System for Sri Lankan Audience Forecasting**

### 🔍 Problem Statement

With the exponential growth of video content on YouTube, understanding and forecasting video performance has become essential for content creators, marketers, and researchers. Despite the vast availability of video analytics on YouTube, there exists a critical gap in tools that can predict video viewership **in specific geographic and cultural contexts**, such as **Sri Lanka**.

This project aims to build a **high-quality, large-scale dataset** of YouTube videos that are relevant to **Sri Lankan audiences**, with the specific goal of enabling downstream tasks such as **predictive modeling** of viewership and **trend analysis**. The dataset will be created by **automated data collection scripts** that interact with the **YouTube Data API v3**, focusing on extracting metadata and early performance indicators across a diverse set of content categories.

This system will serve as the **data foundation** for developing a machine learning model that can forecast video popularity (e.g., expected views within 7 or 30 days) based on its features like publish time, length, category, and early engagement metrics.

---

### 🎯 Objectives

1. **Automate the collection** of public YouTube metadata from channels popular among the Sri Lankan viewer base across multiple categories such as:

   * News & Media
   * Entertainment & Music
   * Education
   * Vlogs & Lifestyle

2. Collect the following types of data in **bulk** using custom scripts:

   * **Video-level metadata**: publish time, category, duration, tags, title, description, etc.
   * **Engagement metrics**: view count, like count, comment count, extracted at multiple time intervals.
   * **Channel-level metadata**: subscriber count, total uploads, country (if available), etc.

3. Ensure the system:

   * **Respects API quotas and rate limits**
   * Can be **run periodically** (e.g., daily or hourly) to track the **evolution of video performance over time**
   * Organizes the collected data into a **clean, structured format** (e.g., CSV or database) suitable for training predictive models.

4. Store and preprocess the dataset to enable **engineering of advanced features** such as:

   * Day/time of publishing
   * Sentiment of title/description
   * Engagement-to-view ratio
   * Category-based performance comparisons
   * Early viewership trends (for videos under 7 days old)

---

### 📦 Expected Dataset Contents

Each video record will include the following:

#### 🧱 Video Metadata

* `video_id`, `title`, `description`, `published_at`, `category_id`, `tags`, `duration`, `thumbnail_url`

#### 📊 Engagement Metrics

* `view_count`, `like_count`, `comment_count`, `engagement_ratio`, `time_since_published`

#### 📡 Channel Metadata

* `channel_id`, `channel_title`, `subscriber_count`, `video_count`, `country`

#### 🧠 Engineered Fields (from preprocessing)

* `publish_day_of_week`, `publish_hour`, `title_length`, `tag_count`, `sentiment_score`, `viewership_class`, `growth_trend`, etc.

---

### 🧠 Why This Matters

* Enables **data-driven insights** into what drives viewership in Sri Lanka.
* Helps **content creators** understand optimal strategies for engagement.
* Offers a **Sri Lanka–centric research-grade dataset** which currently does not exist.
* Provides the **foundation** for forecasting models, interactive dashboards, and content planning tools.

---

### 🛠️ Technical Approach

1. **Seed List Creation**:

   * Identify a list of **Sri Lankan YouTube channels** manually or via Social Blade, YouTube Trends, or local influencer directories.

2. **API Integration**:

   * Use Python and the **`google-api-python-client`** to interface with YouTube Data API v3.
   * Query video and channel endpoints using efficient, paginated API calls.

3. **Periodic Data Tracking**:

   * Implement scripts that **revisit recent videos daily** to track their **view/like/comment growth** over the first 7–30 days (key for modeling).

4. **Data Storage & Processing**:

   * Store data in **CSV**, **JSON**, or **relational database** (e.g., SQLite or PostgreSQL).
   * Schedule regular data pulls using **cron jobs**, **task schedulers**, or **cloud functions**.
You list "CSV, JSON, or relational database." For the MVP, strongly consider committing to a database (like SQLite for development, PostgreSQL for deployment) right away.

Reason: The track_performance.py script will generate a new snapshot file daily. You will quickly have hundreds of CSVs. Querying data across all these files (e.g., "get the full history for video X") will become very complex and slow. Storing all snapshots in a single database table with proper indexes will be far more efficient and scalable.

5. **Preprocessing Pipeline**:

   * Clean raw data
   * Engineer additional features
   * Label targets for prediction

---

### 📈 Long-Term Goal

Enable the training and evaluation of a robust **machine learning model** that predicts video performance based on:

* Metadata available before publishing
* Early engagement metrics
* Channel characteristics

This model and dataset will power the second phase of the project: a **web-based tool** where users can input video details and receive **forecasted viewership metrics**, along with visualizations and strategic content suggestions.

---

## 📁 Project Folder Structure:

### `youtube-forecasting-project/`

```
youtube-forecasting-project/
│
├── 📁 data/
│   ├── raw/                       # Unprocessed raw JSON/CSV from API
│   ├── processed/                 # Cleaned and feature-engineered data
│   ├── snapshots/                 # Time-based view/like tracking snapshots
│   └── logs/                      # Logs for data collection runs and errors
│
├── 📁 scripts/
│   ├── config.py                  # API keys, constants, parameters
│   ├── collect_channels.py       # Gets list of target Sri Lankan channels
│   ├── collect_videos.py         # Gets video metadata and stats per channel
│   ├── track_performance.py      # Daily/periodic engagement updates
│   ├── process_data.py           # Preprocessing, cleaning, feature engineering
│   └── utils.py                  # Common functions (e.g., ISO parser, API wrappers)
│
├── 📁 models/
│   └── forecasting_model.ipynb   # Notebook for training/testing ML models
│
├── 📁 dashboard/
│   └── app.py                    # Streamlit or Flask app for visualization/tool
│
├── 📁 reports/
│   └── project_proposal.md       # Project description, assumptions, goals
│
├── 📄 requirements.txt           # Python packages (API client, pandas, etc.)
├── 📄 README.md                  # Setup and usage instructions
└── 📄 .env                        # Your API key (ignored in version control)
```

---

## 🔧 Key Script Functions

### 1. `config.py`

```python
API_KEY = "YOUR_YOUTUBE_API_KEY"
MAX_RESULTS = 50
SRI_LANKAN_CHANNEL_IDS = [
    "UCXXXXXXX",  # Ada Derana
    "UCYYYYYYY",  # Wasthi
    # Add more manually or scrape via SocialBlade
]
BASE_URL = "https://www.googleapis.com/youtube/v3/"
```

---

### 2. `collect_channels.py`

* Optional: if you're generating a list of Sri Lankan YouTube channels using a keyword/region filter.
* Use `search.list` with `regionCode='LK'`, `type='channel'`, and `relevanceLanguage='en'`.
Your description mentions using search.list with regionCode='LK'. This is a great way to discover new channels, but be very careful: it costs 100 API units per call. For your initial MVP, it's more quota-efficient to rely on a manually curated seed list of 50-100 high-confidence Sri Lankan channels that you build yourselves. You can run the search-based discovery script sparingly later on.
---

### 3. `collect_videos.py`

* For each `channel_id`, call `search.list` to get recent videos
* Then use `videos.list` to get metadata, statistics, and contentDetails (e.g., duration)

```python
def get_recent_videos(channel_id):
    # Get last 50 videos from channel
    pass

def get_video_details(video_ids):
    # Get video-level metadata + stats
    pass
```

✅ Save outputs to `data/raw/videos_{date}.csv`

---

### 4. `track_performance.py`

* Run daily or every few hours to **track change in views/likes/comments**
* Store a daily `snapshot` CSV like: `video_id`, `date`, `views`, `likes`, `comments`

```python
def update_daily_metrics():
    # Load video list from raw data
    # Query API and log daily metrics
    pass
```

✅ Save outputs to `data/snapshots/snapshot_2025-07-21.csv`
Add Robust Error Logging. This script will run automatically. Make sure to wrap your API calls in try...except blocks. If the API returns an error or a video has been deleted, log that error to a file in your data/logs/ directory (e.g., data_collection.log) with a timestamp. This will be invaluable for debugging without having to watch the script run.

---

### 5. `process_data.py`

* Clean data, engineer features (title length, publish time, etc.), and label viewership class

```python
def preprocess_data():
    # Clean NaNs, parse duration, convert timestamps
    # Add derived columns: day_of_week, engagement_ratio, etc.
    pass
```

✅ Save processed output to `data/processed/final_dataset.csv`

---
This is the perfect place to implement the logic for separating Shorts vs. Long-form videos. After loading the raw data, this script can add a new boolean column is_short based on the video's duration. This keeps your collection scripts simple and centralizes the "business logic" in the processing script.
### 6. `utils.py`

* Helper functions like:

```python
def parse_iso_duration(iso_duration):
    # Convert PT12M30S to seconds
    pass

def to_local_time(utc_time):
    # Convert UTC to Sri Lanka Time (UTC+5:30)
    pass
```

---

### 7. `requirements.txt`

```text
google-api-python-client
pandas
numpy
schedule
python-dotenv
textblob
```

---

### 🧪 Bonus (Optional Early Testing Notebook)

```text
notebooks/
├── fetch_sample_data.ipynb       # To test script logic on a few channels
```

---

### 🚀 Run Schedule

Use `cron` on Linux or `Task Scheduler` on Windows to run:

| Script                 | Frequency     | Purpose                                   |
| ---------------------- | ------------- | ----------------------------------------- |
| `collect_videos.py`    | Once per week | Fetch new video metadata                  |
| `track_performance.py` | Daily         | Track view/like/comment changes over time |
| `process_data.py`      | Weekly        | Clean and update feature dataset          |
