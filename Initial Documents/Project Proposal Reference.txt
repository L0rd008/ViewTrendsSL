=======PROJECT PROJECT PROPOSAL========
### 📋 **PROJECT CONTEXT QUESTIONS**

#### 🔹 General Project Context

1. **What is the name or title of your project (tentative or final)?**
ViewTrendSL : YouTube Viewership Forecasting for Sri Lankan Audience using Data Science
2. **How many members are on your team, and what are their names?**
Sanjula N.G.K. 220578A, Senevirathne S.M.P.U. 220599M, Shaamma M.S. 220602U 
3. **Do any of your team members have specialized roles (e.g., frontend, data analysis, backend)?**
No, but Sanjula is good with coding. Senevirathne is the YT specialist(me). (We don't even know 'what' to distribute among each other, as we haven't started working on this, things might be different once we're working, for now what we have to do is plan and come up with ways to collect data since Sri Lanka specific video data is not available)
Senevirathne (The YouTube Specialist): Data Lead

Responsibilities: Lead the data collection strategy. Use your domain knowledge to identify the best Sri Lankan channels to track. Write and manage the Python scripts for the YouTube API. Perform the Exploratory Data Analysis (EDA) to find initial patterns and insights. You are the expert on the data itself.

Sanjula (The Coder): Backend & Model Lead

Responsibilities: Take the cleaned data from Senevirathne and focus on the machine learning pipeline. This includes feature engineering, training different models (XGBoost, etc.), and evaluating them. You will also build the backend API (e.g., using Flask) that serves the trained model.

Shaamma: Frontend & Documentation Lead

Responsibilities: Own the user-facing part of the project. Build the web dashboard using Streamlit or HTML/CSS/JS. Create the data visualizations (graphs, charts) based on the EDA findings and the model's output. You will also take the lead on preparing the final project report and presentation, ensuring all the work is clearly documented.

4. **Will this project continue after the proposal, or is it only a proposal-based evaluation?**
this is a 3 month long project with multiple milestones. project proposal is just the week 3 update. The milestones are(each milestone is one week the current week is: 1. Project Feasibility Document, 2. Project Schedule (Gannt Chart)), Mentor meetup 1, Project Idea Submission, Project Proposal Submission, (1. Project Feasibility Document, 2. Project Schedule (Gannt Chart)),Work on the system requirements, specification and design, (3. System Requirement Specification, 4. System Architecture and Design), Mentor meetup 2, Development Iteration 1, 5. Midevaluation, Development Iteration 2, 6. Testing & Evaluation Document, Mentor meetup 3, 7. Final Evaluation, 8. Final Product Resources submission, 9. Final Report Submission

---

#### 🔹 Problem Understanding

6. **What real-world problem are you trying to solve with YouTube view forecasting?**
Enable Sri Lankan YouTube creators to have a clear idea before uploading, whether it'd perform well or bad. 
7. **Who are the end users or stakeholders for this tool (e.g., content creators, marketers, media companies)?**
This would be useful to anyone, content creators, marketers or media companies, in Sri Lanka. We don't think there is a way to specialize this tool specifically for, say, "content creators"
8. **Why is this problem especially relevant to a Sri Lankan audience or YouTube creators in Sri Lanka?**
This is a university project(University of Moatuwa: In22-S5-CS3501 - Data Science and Engineering Project) that was handed to us as our sem 5 project. Their scope was sri lankan YT, having said that, i think we'd be able to use international datasets too, as sri lanka videos would only have different titles/descriptions/thumbnails, the way people react to content, whether from US, or Sri Lanka would not be very different imo.
9. **Are there any specific pain points you’ve observed in current forecasting methods or tools?**
having a suitable dataset. sri lankan specific data retrieval through YT API V3 is impossible and hence we have to use our quota to search for Sri Lankan keywords to find channels, verify them, and store. After that, we'd have to monitor videos of those channels (i don't think sri lankan channels have been monitored before) for, say, 2 weeks, and collect view counts daily(or hourly: we still haven't decided on which timeframe were going to predict data) and then train models on that. We also don't know if we're going to accept new videos that would be uploaded by the channels in the channel list on the time we're actively started collectingview counts daily(if we do that, the new videos would have fewer data points). we haven't decided how past videos we track(1 month old max/2 week old max/etc)

Prediction Timeframe: Decide on your primary forecast goal. A great start is predicting the view count at specific future intervals: 24 hours, 3 days, and 7 days after upload. This is manageable and highly valuable.

Data Collection Strategy:

Historical Data (One-Time Scrape): For your initial dataset, collect metadata for all videos published in the last 6-12 months from your target channels. This gives your model a robust understanding of what features lead to long-term success.

Time-Series Data (Continuous Tracking): For a smaller, more recent set of videos (e.g., all new videos published from your start date onwards), you must track their view count over time. Poll the YouTube API for their view counts every 6-12 hours for the first 30 days. This data is essential for understanding the shape of viewership growth and for training your models to predict those 24-hour, 3-day, and 7-day targets.

Handling New Videos: Yes, absolutely accept new videos. Your automated script should check for new videos from your channel list daily. When a new video is found, add it to your "active tracking" database to start collecting its view count snapshots.

---

#### 🔹 Data Collection & Sources

10. **Have you already collected any YouTube data? If so, how much and what format is it in (CSV, JSON, SQL)?**
yes, JSON(channels), CSV(videos), but no collection is finalized(since we still don't know what features we'd actually use)
11. **What categories of Sri Lankan YouTube channels are you focusing on (e.g., news, music, education)?**
ALL types
12. **Will the data be collected only through the YouTube Data API v3, or do you plan to use any additional sources (e.g., Social Blade, Kaggle datasets)?**
mainly YT API, but if that's not enough we'd be willing to use other sources(but we don't know what to use and when to use)
13. **What variables will you include in your dataset (e.g., views, likes, video duration, publish time, comments, etc.)?**
still not sure as we just started. views/likes/video duration/publish time(and day of the week)/description/title for sure. Currently we're collecting everything we can(so that we can just disregard what we won't use)
14. **Will you include only Sri Lankan videos/channels? If yes, how do you identify whether a video is Sri Lankan?**
not sure. I think we'd be able to use international videos too for a generally good accuracy. still not decided. to identify sri lankan channels, we are using a keyword set(sri lankan words, doing search queries and use the results to identify sri lankan channels, then monitor the videos of those channels)

Your intuition that user behavior is universal is partly true, but the YouTube algorithm is highly localized. Viewing habits, popular topics, prime-time hours, and language are all specific to a region.

Recommendation for MVP: Focus exclusively on Sri Lankan channels and content. This will make your model much more accurate for your target audience. Mixing in global data will introduce noise and confuse the model, as the factors driving a MrBeast video's success are very different from those driving a local Sri Lankan news report.

How to Identify:

Start with a manually curated list of known Sri Lankan channels.

Check the country code in the channel's metadata from the API.

Use a language detection library on titles/descriptions to find content primarily in Sinhala or Tamil.

Combining these will give you a high-quality, relevant dataset.

---

#### 🔹 Methodology and Tools

15. **What tools and libraries do you plan to use? (e.g., Pandas, Scikit-learn, XGBoost, Streamlit, Flask, SQL, etc.)**
currently streamlit, sqlite3, json, pandas, numpy, scipy,Scikit-learn, XGBoost, jupyter, pytrends, plotly, seaborn,matplotlib, schedule, APSchedule, nltk, textblob, YT API libs, python dotenv, pytz, isodate, tqdm, pydantic, etc
16. **Do you plan to build a web-based forecasting tool, or will it just be a local prototype?**
we will create a web based forcasting tool, host it. our mentor has the idea to publish the application, as well as the dataset, alongside a research paper
17. **What kind of predictive model(s) are you planning to use (regression, classification, ensemble, etc.)?**
not decided. maybe time series, maybe regression, maybe ensemble.
This is a Regression Problem, not a traditional Time-Series Problem. You are not forecasting the next step of a single known time series. Instead, you are predicting the future performance of a new video based on its initial features (title, category, channel stats, etc.).

Recommended Model Type: Ensemble models are perfect for this. Specifically, start with a Gradient Boosting model like XGBoost or LightGBM. They are state-of-the-art for tabular data, handle mixed data types well, are robust to outliers, and can tell you which features are most important.

How to Generate the Forecast Graph: Instead of a complex time-series model, you can build a few simpler regression models:

Model 1 predicts views_at_24_hours.

Model 2 predicts views_at_3_days.

Model 3 predicts views_at_7_days.
Your web application then takes these predicted points and plots a curve through them. This approach is much more feasible and robust for your MVP.

18. **Do you plan to use time-series forecasting models (e.g., ARIMA, Prophet), or is your model feature-based (e.g., Random Forest)?**
yes, i think we would need to do that

---

#### 🔹 Evaluation & Output

19. **How will you evaluate the accuracy or quality of your predictions (e.g., RMSE, MAE, user testing, dashboard usability)?**
we'll need a new method. we aim to show the output/prediction as a graph. (say, with 100 datapoints) so all the 100 datapoints would have an effect on the evaluation. each should be taken into account when calculating accuracy.

Recommended Evaluation Metrics:

MAPE (Mean Absolute Percentage Error): This is the best for your use case. It answers the question, "On average, what percentage is our forecast off by?" A MAPE of 20% means you are, on average, 80% accurate, which is an excellent result for this kind of problem.

RMSE (Root Mean Squared Error): This measures the average magnitude of the error in the actual number of views. It's useful but harder to interpret across videos with vastly different view counts.

How to Apply: You will calculate these metrics for each of your prediction points (e.g., calculate MAPE for the 24-hour prediction, MAPE for the 7-day prediction, etc.). This gives you a clear and standard way to measure and report your model's performance.

20. **What would you consider a successful outcome for the project (e.g., <10% prediction error, functional dashboard, 5 case studies on Sri Lankan videos)?**
maybe 85%+ accuracy(is this justified as a sem 5 project, not a multi million dollar funded project, also considering YT algorithm change)(when we collect data for a month, we also might need to collect data of a previous year, to take the algorithm change over years, into account. also the timeframe, ie the fact if we collect data of a continuous month or a year, should not introduce bias, so it should not be like a year imo) we need a functional dashboard, yes. 
Realistic Goal: An "85% accuracy" target translates to a MAPE of 15%. For a university project predicting a chaotic system like YouTube views, this is extremely ambitious. A more realistic and still very successful goal would be: "Achieve a Mean Absolute Percentage Error (MAPE) of less than 30% for 7-day view forecasts on our held-out test dataset." This is a specific, measurable, and impressive result.

Regarding Algorithm Changes: Your idea to use data from previous years is smart but complex. For the MVP, focus on data from the last 6-12 months. This is a good compromise, as it's recent enough to reflect the current algorithm's general behavior while still providing enough data. Acknowledge "algorithm drift" as a limitation in your final report.
