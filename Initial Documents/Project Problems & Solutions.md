## 🧠 MASTER QUESTION SET FOR “VIEWTRENDSL”
---

### 🔹 1. DATA COLLECTION STRATEGY

**A. Scope and Source**

1. Will we collect only public YouTube video stats (views, likes, etc.) or also analyze content (thumbnails, titles, transcripts)?
For the MVP, focus exclusively on public video metadata (views, likes, comments, title, description, tags, category, duration, publish time). Analyzing thumbnails, audio, or transcripts requires complex computer vision and NLP models. This is a perfect "Version 2.0" feature.
2. Should we focus on only Sri Lankan creators or include global channels targeting Sri Lankan audiences?
Start with a curated list of 100-200 popular Sri Lankan channels across various categories. This creates a focused, high-quality dataset. Including global channels targeting Sri Lanka is a good idea for later expansion, but it's hard to define that target audience accurately initially.
3. Will we separate data by:

   * Shorts vs Longs?
Absolutely, yes. These are fundamentally different. Their view patterns, discovery methods, and engagement metrics are not comparable. You should treat them as two separate datasets and likely build two separate models.
   * Language (Sinhala, Tamil, English)?
Yes. Add a language column (e.g., 'Sinhala', 'Tamil', 'English') based on the channel or title/description analysis. This will be a powerful feature.
   * Category (News, Music, Education, etc.)?
Yes, this is a critical feature provided directly by the API.

**B. Timeline and Frequency**
4\. Do we want to scrape/upload historical data (e.g. views over 6 months)?
Yes. The best approach for your MVP is a one-time, large-scale data collection. Aim to get data for videos published in the last 6-12 months. This gives you a good range of video ages to see how view counts mature over time.
5\. Should we continuously collect data (e.g. hourly/daily polling) or is a one-time dump enough?
For the MVP, a one-time data dump is more practical. Set up a script to run for several days to gather this historical data. Then, for the forecasting part, you will need to track a smaller, newer set of videos daily/hourly.
* Recommendation:
1.  Historical Scrape (One-time): Collect metadata for thousands of videos published in the last year.
2.  Active Tracking (For forecasting): From your channel list, fetch any new videos published daily. For these new videos, run a script every few hours (e.g., every 6 hours) to log their viewCount, likeCount, etc. Do this for at least 2-4 weeks. This creates the time-series data needed for prediction.
6\. How frequently will we update the dataset once deployed (daily, weekly, monthly)?
A weekly or bi-weekly batch process to re-train the model would be a good balance between keeping the model fresh and managing API/compute costs.

**C. APIs and Methods**
7\. Which APIs will we use? Only the YouTube Data API? Any third-party APIs for thumbnails/audio/transcripts/SEO?
For the MVP, stick to the YouTube Data API v3. It's free (within quota) and provides all the core metadata you need. Keep other APIs (Social Blade, audio analysis) on the "Future Enhancements" list.
8\. What quotas and limits will affect our scraping (per day/per key/per user)?
The standard YouTube Data API v3 quota is 10,000 units per day. A videos.list call costs 1 unit, a search.list costs 100 units. Be very careful with search calls. Getting videos from a channel's playlist is much cheaper (1 unit per page).
9\. Do we need multiple API keys (via user login or multiple Google accounts) to increase quota?
Yes, this is a common strategy. You have 3 team members, so you can register 3 separate Google Cloud projects to get 3 API keys. This triples your daily quota to 30,000 units, which will be essential for the initial data collection.

**D. Automation**
10\. Can we automate:

* Dataset updates?
Yes. Use a scheduler library (APScheduler in Python is great) or a simple cron job on a server to run your data collection scripts automatically.
* Re-training ML models?
Yes. This can be automated. After a new batch of data is collected and cleaned, a script can trigger model retraining and evaluation.
* Feature extraction?
Yes. This should be a core part of your data processing pipeline. As soon as new data comes in, it should be automatically cleaned and features should be extracted.

---

### 🔹 2. DATA STRUCTURE & MODELING

**A. Core Entities**
11\. What are the core entities in our data? (Video, Channel, Category, Time Snapshot, User Session?)
* Channel: Stores channel-level info (ID, name, subscriber count).
* Video: Stores static video info (ID, title, description, duration, is_short, channel_id, category_id).
* Snapshot: This is key for time-series. It stores video_id, timestamp, view_count, like_count, comment_count.
* Tag: Stores unique tags.
* VideoTag (Junction Table): Links videos to tags (many-to-many).
12\. How will Shorts and Longs be modeled differently?
Model them with a boolean flag (is_short) in the Video table. In your analysis and modeling, you will use this flag to filter and train separate models.
13\. Do we need metadata on:
* Uploader’s location: Yes, the channel's country is available from the API and is a very useful feature.
* Content tags: Yes, crucial for understanding topic. Store them.
* SEO fields: Title and description are your primary SEO fields.

**B. Relationships**
14\. What are the relationships between:
* Videos and Channels: One-to-Many (One Channel has many Videos).
* Users and Searches: This is part of your application's logic, not the core YouTube data model. A User table could have a SearchHistory table linked to it.
* Categories and View patterns: This is not a direct database relationship, but an analytical one you will discover during EDA.

**C. Database Design**
15\. Will we use SQLite for dev and PostgreSQL for prod?
 Yes, SQLite for development and PostgreSQL for production is an excellent and standard choice. SQLite is simple and file-based. PostgreSQL is robust, scalable, and handles concurrent connections well, which is vital for a web app.
16\. How will we model many-to-many relationships (e.g. videos with multiple tags)?
Use a junction table (also called a linking table). For example:
* Videos table (video_id, title, ...)
* Tags table (tag_id, tag_name)
* Video_Tags table (video_id, tag_id)
17\. What indexing or partitioning strategies will optimize speed for large datasets?
For the Snapshot table, create a composite index on (video_id, timestamp). This will make lookups for a specific video's history incredibly fast. Index foreign keys (channel_id, category_id) as well.

---

### 🔹 3. DATA PREPROCESSING & FEATURE ENGINEERING

**A. Cleaning**
18\. How will we handle missing fields (e.g. likes disabled, comments off)?
* Disabled likes/comments: Impute with 0. You can also create a boolean feature like comments_disabled (1 or 0), as this itself can be a predictive signal.
19\. How to normalize time-based stats (e.g. views/day)?
This is critical. Don't use raw view counts. Create features like:
* views_in_first_24h
* views_per_hour (for the initial period)
* likes_per_1000_views
20\. Should we remove outliers (e.g. celebrity videos that go viral)?
Do not remove them initially. Viral videos are exactly what you want to understand! Instead, use models that are robust to outliers (like tree-based models) and use transformations like the log transform (np.log1p(x)) on view counts to handle the skewness.

**B. Feature Extraction**
21\. What features will we extract:
* Title: title_length, num_capital_letters, num_exclamation_marks, contains_sinhala (boolean), contains_question (boolean).
* Thumbnail: (Future) Brightness, contrast, presence of faces.
* Audio/Video: (Future) Speech-to-text on transcript, sentiment analysis of transcript.

22. What time-based features might help (e.g., day of week, time posted, trend slope)?
Absolutely! These are very powerful.
* publish_hour_of_day
* publish_day_of_week
* publish_is_weekend
* Growth Velocity: (views_at_24h - views_at_6h) / 18. This captures the initial acceleration.
**C. Feature Selection**
23\. Which features are potentially highly correlated or redundant?
likeCount and commentCount will be highly correlated with viewCount. This is okay for tree-based models but can be an issue for linear models. A correlation heatmap will reveal this.
24\. Should we use dimensionality reduction (PCA/TSNE) or manual feature selection?
For the MVP, manual feature selection and feature importance from a Random Forest/XGBoost model is the best approach. It's faster and more interpretable than PCA.

---

### 🔹 4. EXPLORATORY DATA ANALYSIS (EDA)

25. What are the most common growth shapes of YouTube views?
The common patterns are:

Spike & Decay: Typical for news or trend-based content.

Slow Burn: Evergreen content (tutorials, educational) that grows steadily over time.

Flatline: Videos that fail to gain traction.
26. What patterns emerge between view counts and:

* Category?
* Upload time?
* Title/thumbnail characteristics?
This is the core of your EDA. Use visualizations to explore these relationships:

Box plots: Views by category or day of the week.

Scatter plots: Video duration vs. views.

Time-series plots: For individual videos, overlaying several to see patterns.
27. Can we group videos using unsupervised clustering?
Excellent idea. Use a clustering algorithm like K-Means on the normalized time-series data of videos to automatically group them into the growth patterns described above. This can become a predictive feature itself ("Predicted Growth Type").
---

### 🔹 5. MODELING & FORECASTING

**A. Model Objectives**
28\. Do we want to:

* Predict total views after X days?
* Predict view counts over time (time series)?
* Classify video growth pattern types?
For the MVP, the most practical approach is predicting total views after specific time intervals (e.g., 24 hours, 7 days, 30 days). This turns the problem into a standard regression task, which is easier to start with than a full time-series forecast. The output graph can then be constructed from these key prediction points.
**B. Separate Models**
29\. Will we train different models for:

* Shorts vs Longs?
* Categories?
* Timeframes?
Yes. At a minimum, have two main models: one for Shorts and one for Long-form videos. Their behavior is too different to combine. You can include "Category" as a feature in each of these models rather than building separate models for every single category, which would be too complex.
**C. ML Models**
30\. Will we use:

* Traditional ML (XGBoost, Random Forest)?
* Time Series (ARIMA, Prophet)?
* Deep Learning (LSTMs, Transformers)?
* Hybrid models?
Start with XGBoost or LightGBM. They are powerful, fast, and work exceptionally well on the kind of tabular, heterogeneous data you'll have. Time-series models like ARIMA are not suitable here because they are designed for forecasting a single series, not for predicting a new, unseen series based on its initial features. LSTMs are overkill for the MVP.
31. What metrics will we use to evaluate accuracy (RMSE, MAPE, etc.)?
* RMSE (Root Mean Squared Error): Good, but penalizes large errors heavily.
* MAE (Mean Absolute Error): More interpretable (e.g., "on average, our prediction is off by X views").
* MAPE (Mean Absolute Percentage Error): Very useful for this problem. "On average, our prediction is off by X%." An 85% accuracy target likely means a MAPE of 15% or less.
32. How often will we retrain the models? With what volume of new data?
For the MVP, train once on your historical dataset. For a production system, you would retrain weekly or monthly with the newly collected data.
33. Will we store older models to compare performance over time?
Yes, this is great practice. Version your models (e.g., model_v1.pkl, model_v2.pkl) and log their performance metrics. This allows you to track improvements and revert if a new model performs worse.
---

### 🔹 6. SYSTEM ARCHITECTURE

34. How will the backend connect with the ML models (via API, embedded Python)?
Use a REST API architecture. Your machine learning model, once trained, should be saved as a single file (e.g., using joblib or pickle). Your backend (built with Flask or a similar framework) will load this file when it starts. When a prediction request comes in, the backend preprocesses the input data, passes it to the loaded model's .predict() method, and sends the result back as a JSON response. This decouples your model from the application logic.
35. Should predictions be generated in real-time or batch-wise?
Predictions should be real-time (on-demand) from the user's perspective. A user inputs a video's details and gets a forecast back within seconds. The "batch" part of your system should be the data collection and model re-training, which happens in the background on a schedule.
36. How scalable is the backend (can we handle hundreds of concurrent queries)?
For the MVP, a single server instance on a cloud provider will be sufficient. The key to future scalability is a stateless API. This means your Flask application doesn't store any information between requests. All state is in the database or cache. This design allows you to easily add more server instances behind a load balancer as your user base grows.
37. Will we use containerization (Docker) for deployment?
Highly Recommended. Using Docker will solve the classic "it works on my machine" problem. It bundles your application, its dependencies, and the trained model into a single, portable container. This makes moving from your local development laptops to a cloud server incredibly simple and reliable. It is an excellent skill for your team to learn.

---

### 🔹 7. FUNCTIONALITIES (USER FEATURES)

**A. Roles & Access**
38\. What are the user roles (Free, Pro, Admin)?
Keep it simple. Start with a single, free user type to demonstrate all core functionality. You can describe the "Free vs. Pro" model in your documentation as a future business plan. If you must implement roles, consider:

Free/Creator: Can perform maybe 3-5 forecasts per day.

Pro/Analyst: Unlimited forecasts, access to deeper analytics (this can be mocked up for the demo).

Admin: (You and your team) Internal dashboard to monitor system health and usage.


39\. What features are available per tier (e.g. historical prediction depth, export, model transparency)?
Free Tier: Core functionality – input a video URL, get a view forecast graph for the next 7 days.

Pro Tier (Future Plan): Longer-term forecasts (30/60/90 days), comparison features, competitor analysis, SEO suggestions, data export.

**B. Core Features**
40\. Can users:

Input a YouTube link and get a forecast? Yes, this is the absolute core function of the MVP.

See historical view growth? Yes, your tool should show the actual view count up to the present moment, and then the forecasted growth.

Compare multiple videos/channels? This is an excellent feature, but probably best for post-MVP. Focus on perfecting the single-video forecast first.

Filter by category, date, language? This is more for the analytical dashboard you will build, which displays insights from your overall dataset.

**C. Extra Features**
41\. Do we allow:

Dataset export? Yes, as a "Pro" feature or for your research goal.

API access? This is a great future monetization path, but out of scope for the MVP.

Chrome Extension integration? Excellent idea for the future, but a separate project in itself.

SEO recommendations? This would be a key "Pro" feature, using insights from your model (e.g., "Titles with questions perform 15% better in this category").

---

### 🔹 8. LEGAL, PRIVACY & COMPLIANCE

42. Are we violating YouTube TOS by storing video analytics?
Generally, using the public YouTube Data API for analysis and displaying aggregated/derived data (like a forecast) is acceptable. However, you are not allowed to publicly display raw API data for extended periods or allow users to download it. You must also link back to YouTube's Terms of Service. It is critical that your team reads the YouTube API Services Terms of Service carefully.
43. Are we collecting any user data from those who access our app?
If you implement a login system (e.g., with email/password), you are collecting Personally Identifiable Information (PII). You will need a Privacy Policy page explaining what you collect and why. For the MVP, you could avoid this by not having user accounts.
44. Do we need disclaimers for predictions (e.g., "not 100% accurate")?
Absolutely, yes. Every prediction must be accompanied by a clear disclaimer. For example: "This is a statistical forecast based on historical data and is not a guarantee of future performance. Actual views may vary." This manages user expectations and reduces liability.

---

### 🔹 9. PERFORMANCE & OPTIMIZATION

45. How do we ensure fast response times for predictions?
Caching is your best friend. If someone requests a forecast for a video you've already analyzed, serve the result from a cache instead of re-running the entire model. Use a system like Redis for this in production, or a simple in-memory dictionary for the MVP.

Optimize your feature extraction code to be as fast as possible.

Keep the model itself relatively lightweight (XGBoost is good for this).
46. Will we cache results of previously analyzed videos?
Yes. This is the single most important optimization you can make for user-perceived performance. Cache the final prediction keyed by the video ID.
47. Can we use GPU acceleration for training?
For model training, GPU acceleration is very beneficial for deep learning models (LSTMs, etc.). For XGBoost, a powerful CPU is often more important. For model inference (making a single prediction), a CPU is perfectly sufficient and you will not need a GPU on your production server for the MVP.

---

### 🔹 10. FUTURE EXTENSIONS & RESEARCH

48. Can we plug in audio/image sentiment analysis to improve predictions?
Yes, this is an excellent direction for future research. Analyzing thumbnail composition (e.g., color saturation, presence of faces, text) and audio sentiment could provide powerful features to improve prediction accuracy.
49. Should we add a community voting/rating system for videos?
This is a large feature that changes the nature of your product from a utility tool to a community platform. It would require user management, content moderation, and significant database changes. I would suggest keeping this as a distant, "maybe-someday" idea.
50. Should we publish anonymized data for researchers?
Absolutely. This aligns perfectly with your academic goals. Anonymize it by removing any PII (like specific user comments) and perhaps even hashing channel/video IDs. This would be a valuable contribution to the data science community.


### **Practical Problems & Challenges for ViewTrendSL**

#### **Category 1: Data Collection & Integrity**

1.  **The Quota Catastrophe:**
    * **Problem:** You have a daily limit of 10,000 API units per key. A single `search` query costs 100 units. Your team could easily burn through the entire daily quota (even with 3 keys) in just a few hours of aggressive, unoptimized scraping, completely halting data collection for 24 hours.
    * **Impact:** This will severely delay building your initial dataset, which is the foundation of the entire project.
Solution: Smart & Efficient API Usage.

Avoid search.list: This is your biggest quota killer (100 units). Instead, manually curate your list of Sri Lankan channels. Use the channel's uploads playlist ID with the playlistItems.list endpoint (1 unit) to get all their video IDs. This is 100x more efficient.

Cache API Responses: Before making any API call, check if you already have that data in your local database. For the initial scrape, store the raw JSON response for each video. This prevents re-fetching the same data if your script fails and needs to be restarted.

Implement Rate Limiting: Add time.sleep(1) between API calls in your script. It will slow down the collection slightly but makes it much less likely you'll hit a rapid-fire rate limit.

Rotate API Keys: Write your script to cycle through your team's three API keys. If one hits its limit, the script automatically switches to the next one.

2.  **The "Sri Lankan" Identity Crisis:**
    * **Problem:** You plan to use keywords to identify Sri Lankan channels. What happens when a global channel uses "Sri Lanka" in a title for a travel vlog? Or a Sri Lankan creator living abroad makes content for a global audience? Your keyword-based approach will pull in irrelevant data and miss relevant channels, biasing your dataset.
    * **Impact:** The model might learn incorrect patterns, leading to poor predictions for your actual target audience.
Solution: A Multi-Factor Scoring System.

Seed List: Start with a "Gold Standard" list of 50-100 channels you are certain are Sri Lankan. This is your core training set.

API Country Code: When fetching channel data, prioritize those where channel.snippet.country is "LK".

Language Detection: Use a Python library like langdetect or pycld3 on the channel's description and titles of its top 10 videos. If a high percentage of the text is Sinhala (si) or Tamil (ta), it's a strong positive signal.

Create a Confidence Score: Combine these factors. A channel with country='LK' and a high percentage of Sinhala/Tamil text gets a high score. A channel with no country code but some Sinhala keywords gets a medium score. This allows you to filter your dataset with much higher accuracy than keywords alone.

3.  **The Disappearing Data Point:**
    * **Problem:** You start tracking a new video. For the first 3 days, it has views, likes, and comments. On day 4, the creator disables comments. Your data collection script, expecting a `commentCount` field, might crash or start recording null/zero values.
    * **Impact:** This creates "holes" in your time-series data, making it difficult to train a model that relies on consistent features over time. You'll need robust error handling and imputation strategies.
Solution: Defensive Data Ingestion.

Safe Dictionary Access: When parsing the JSON response from the API, use the .get() method with a default value. For example: comment_count = statistics.get('commentCount', 0). If the key is missing, it will assign 0 instead of crashing.

Create Indicator Features: Create new boolean columns in your dataset like comments_disabled or likes_hidden. This turns the missing data into a useful feature. A creator disabling comments is a strong signal that might influence viewership patterns.

4.  **The Shorts vs. Long-form Dilemma:**
    * **Problem:** You've decided to treat Shorts and Long-form videos separately, which is smart. However, the YouTube API doesn't have a simple boolean flag `is_short`. You have to infer it from the video's duration (typically <60 seconds) and sometimes its aspect ratio. This inference can be imperfect.
    * **Impact:** Misclassifying videos will contaminate both datasets, leading to less accurate models for both formats.
Solution: A Two-Factor Rule.

In your data processing script, create a column named is_short.

The rule is: A video is a Short if its duration is less than or equal to 61 seconds AND its aspect ratio (height/width) is greater than 1.

You can get the duration from the contentDetails.duration field (you'll need to parse the ISO 8601 format). You can get height/width from the fileDetails part, but this costs extra quota. For the MVP, just using duration <= 61 seconds is a reliable and cheap proxy.

#### **Category 2: Modeling & Feature Engineering**

5.  **The "Looking into the Future" Leakage:**
    * **Problem:** Your goal is to predict a video's performance *at the moment of upload*. When training your model, you might accidentally include features that wouldn't be available at that time. For example, using the `like_count` after 24 hours as a feature to predict the `view_count` at 24 hours. This is data leakage and will make your model look amazing in testing but perform terribly in the real world.
    * **Impact:** A model with 99% accuracy during development that is completely useless in production because it relies on future information.
Solution: The "Time Zero" Feature Set.

Strictly define your features (X) as only the information available at the moment of upload. This includes:

Video Features: Title, description, tags, category, duration, is_short.

Channel Features: Subscriber count, total video count, channel age.

Time Features: publish_day_of_week, publish_hour_of_day.

Your target variable (y) is the view_count at a future point (e.g., views_at_day_7). Any data collected after upload (like views at 1 hour, 6 hours, etc.) can be used for more advanced models later, but for the initial prediction, they must be excluded to prevent data leakage.

6.  **The "Evergreen vs. Viral" Conundrum:**
    * **Problem:** Your model is trained on a mix of videos: some get a huge spike in views in the first 48 hours (e.g., news), while others grow slowly and steadily for months (e.g., educational tutorials). A single model may struggle to predict both patterns accurately.
    * **Impact:** Your model might consistently over-predict for evergreen content and under-predict for viral content, making it unreliable for different types of creators.
Solution: Feature Engineering and Clustering.

Engineer "Content Type" Features: Create features from the title and tags that hint at the video type. For example, is_tutorial (if "how to" is in the title), is_news (if channel is a news channel), is_music (if category is Music).

Cluster Growth Patterns: For your training data, take the first 24 hours of view data for each video. Normalize it (e.g., as a percentage of the 24-hour total). Use a clustering algorithm like K-Means to group these growth curves into 3-4 patterns (e.g., "Fast Spike," "Slow & Steady," "Delayed Takeoff"). This cluster ID becomes a powerful categorical feature for your model.

7.  **The "85% Accuracy" Mirage:**
    * **Problem:** You've set a goal of "85% accuracy." For a regression problem (predicting a number like view count), this metric is ambiguous. If a video gets 100 views and you predict 85, is that 85% accurate? What if it gets 1,000,000 views and you predict 850,000? The second error is much larger in absolute terms.
    * **Impact:** The team might chase an ill-defined target. You need to switch to standard regression metrics like **Mean Absolute Percentage Error (MAPE)** or **Root Mean Squared Error (RMSE)** to have a clear, measurable goal.
Solution: Adopt Standard Regression Metrics.

Primary Metric: MAPE (Mean Absolute Percentage Error). This is the most intuitive. A MAPE of 20% means your forecast is, on average, off by 20%. An 85% "accuracy" would be equivalent to a 15% MAPE, which is a very ambitious but good target.

Secondary Metric: MAE (Mean Absolute Error). This tells you the average error in absolute views (e.g., "we are off by 5,000 views"). It's good for understanding the scale of the error.

Goal Setting: Set a realistic MVP goal: "Achieve a MAPE of under 35% for 7-day view forecasts on our test set."

#### **Category 3: Technical & Architectural Hurdles**

8.  **The "It Works on My Machine" Curse:**
    * **Problem:** Sanjula develops a feature on Windows using Python 3.9. Senevirathne tries to run it on Ubuntu with Python 3.10, and a key library (`pandas` or `scipy`) behaves slightly differently or fails to install. Now you're debugging environments instead of building the product.
    * **Impact:** Lost development time and immense frustration. This is precisely what **Docker** is designed to prevent.
The "It Works on My Machine" Curse

Solution: Dockerize Your Environment.

Create a Dockerfile in your project root. This file will define the base Python image, copy your code, and install dependencies from a requirements.txt file.

Create a requirements.txt file by running pip freeze > requirements.txt in your virtual environment.

All team members should install Docker and run the project using docker-compose up. This ensures everyone, and the final server, runs on the exact same environment.

9.  **The Heavy Model, Skinny Server Problem:**
    * **Problem:** Your trained XGBoost model file (`model.pkl`) is 400MB. When you deploy your Flask app to a free or cheap cloud server with only 512MB or 1GB of RAM, loading the model into memory either fails or leaves no room for the web server to handle requests.
    * **Impact:** Your application will be slow, crash frequently, or won't even start. You'll need to consider model quantization or choose a more memory-efficient model if this becomes an issue.
Solution: Prioritize Model Efficiency.

Use LightGBM: It is known for being faster and more memory-efficient than XGBoost with similar performance.

Tune for Simplicity: When training your model, deliberately limit its complexity. Reduce max_depth and n_estimators. You might sacrifice 1-2% accuracy for a model that is 5x smaller and faster.

Check Model Size: After saving your model, check the file size. If it's over 100MB, you should investigate optimization.

10. **The Slow Prediction Bottleneck:**
    * **Problem:** A user submits a video URL. Your backend has to: 1) Call the YouTube API (slow), 2) Preprocess the data (can be slow), 3) Run the model (can be slow), 4) Generate graph data (can be slow). The user is staring at a loading spinner for 30 seconds.
    * **Impact:** Poor user experience. Users will assume the app is broken and leave. Implementing a **caching** strategy is non-negotiable.
Solution: Implement Caching.

Use a simple Python dictionary as a cache for your MVP. When a request for a video forecast comes in:

Create a unique key (e.g., video_id).

Check if this key is in your cache dictionary.

If yes, return the cached result immediately.

If no, perform the API calls and model prediction, store the result in the cache with a timestamp, and then return it.

You can add a rule to clear the cache for a video every 24 hours to keep data fresh.

#### **Category 4: Project Management & Team Dynamics**

11. **Scope Creep Temptation:**
    * **Problem:** Your "future plans" list is exciting and full of great ideas (SEO tools, competitor analysis, AI content suggestions). A team member might start building a "cool" but non-essential feature before the core prediction engine is even working reliably.
    * **Impact:** You run out of your 3-month timeline with a lot of half-finished features and a non-functional MVP. You must be ruthless about sticking to the MVP scope first.
Solution: The "MVP / V2 / Backlog" Board.

Use a physical whiteboard or a digital tool like Trello. Create three columns: MVP (Must-Have), V2 (Important, But Later), and Backlog (Nice Ideas).

MVP Column: Should only contain the absolute essentials: Data collection script, one model (for long-form videos), and a basic web page to input a URL and see a graph.

When anyone has a new idea (e.g., "Let's add a competitor analysis tool!"), it automatically goes into the Backlog. The team can vote later to move it to V2, but it cannot be added to the MVP column unless something else is removed.

12. **The Unowned Task:**
    * **Problem:** Everyone assumes someone else is responsible for a critical but unglamorous task, like setting up the deployment server, writing the documentation, or managing the API keys. In the final week, you realize no one has done it.
    * **Impact:** A last-minute scramble, potential project failure, and team friction. **Action:** Assign clear ownership for each major component (Data, Model, Backend, Frontend, DevOps/Deployment).
Solution: Role-Based Ownership. Based on your team's skills, assign clear ownership:

Senevirathne (YT Specialist): Data Owner. Responsible for the entire data pipeline: writing/running collection scripts, cleaning data, and performing EDA.

Sanjula (Coding Strength): Model & Backend Owner. Responsible for feature engineering, training/evaluating the ML models, building the Flask API, and creating the Dockerfile.

Shaamma: Frontend & Presentation Owner. Responsible for building the user interface (Streamlit or HTML/CSS/JS) that consumes the Flask API, creating the final project report, and preparing the presentation slides.
This doesn't mean they work in silos, but it ensures someone is ultimately responsible for getting each major part done.