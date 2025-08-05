====Project description and Minimum Viable Product specifications====

YouTube Video Viewership Forecasting Model for Sri Lankan Viewer Base


 This project aims to develop a data-driven tool that forecasts the viewership of 
YouTube videos, with a specific focus on the Sri Lankan viewer base.
 Students will utilize the YouTube Data API v3 to collect a real-world dataset of 
public YouTube videos, focusing on channels that are popular in Sri Lanka 
across multiple categories such as news, entertainment, education, and 
lifestyle. The collected data will include video metadata such as publish time, 
category, duration, views, likes, comments, and channel statistics.
 Tasks
 •        Data Collection - Use the YouTube API to extract video-level and 
channel-level data relevant to the Sri Lankan audience.
 •        Data Analysis - Perform comprehensive data cleaning, preprocessing, 
and visualization to uncover patterns in video viewership behavior. Analyze 
variables such as publishing time, day of the week, video length, and content 
category about video performance.
 •        Forecasting Model - Build a model to forecast viewership trends for 
videos given specific features like category, target audience, and historical 
engagement and the video.
 •        Tool Development - Build a web-based system that allows users to input 
video metadata and get forecasting for viewership and view the results of data 
analysis (e.g., dashboard).
 Resources:
 https://developers.google.com/youtube/v3/getting-started
 https://arxiv.org/html/2503.04446v1
 https://www.sciencedirect.com/science/article/abs/pii/S0969698924000742

Outcomes:
•        A clean, labelled dataset of Sri Lanka–focused 
YouTube video analytics.
 •        A forecasting model capable of estimating expected 
views for a video based on its metadata and the video 
content.
 •        A web-based tool demonstrating data analysis and 
predictive model functionality.
 •        A comprehensive project report and presentation 
documenting the methodology, findings, and limitations.


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

=======SRS=======

## 1. Introduction

### 1.1 Purpose

4. Who is the intended audience of this document? (e.g., developers, clients, testers, stakeholders)
YouTubers, Influencers, Creators, Producers, Artists, Media Channels, etc
5. Is this document limited to the forecasting module only or the full system (including dashboard, backend, etc.)?
It's intended to be a hosted full system with frontend dashboard for forecasting, backend and DB. But the most important part is the forecasting module. There are intentions to publish this system as a product, create a research paper, and develop a useful dataset.

### 1.2 Scope

6. What are the boundaries of the system? What is explicitly included and excluded?
Forecasting view counts for Sri Lankan videos before uploading. However, it could also be used for international videos, as the features that distinguish a Sri Lankan video from an international video might not have a significant impact on the view count of a video. Can forecast for upto 6 months for a video (based on "A YouTube video's view count typically plateaus within 2-4 months for smaller channels and 2 weeks for larger channels."). So, data collection might need data from at least 6 months(could be different for shorts and long-form as they take separate times to complete the sudden view spike and to plateau. If we can analyse the trends/gradients of the two separate parts of videos: sudden initial spike, and plateau, prediction would be easy. But a remark, the only view-time graph is not spike then plateau, there are many more, and it would be better if we can recognize and analyse them also. it's(spike then plateau) just the most common. even that too differs in how they behave among long form and short form videos). To reduce the bias of the differences/updates to the YT algorithm over the years, we can collect at least 6 months of data of a few years. System should analyse the transcript of the video to be uploaded, content of the video, thumbnail of the video, length of the video, content type of the video, word count per minute, audio analysis, shot switch rate, etc. and give suggestions for optimal performance. For this the ML should be trained on the above mentioned features and more. (We might need many other APIs)

Also we could be able to use social blade to identify top channels by country. Even though current predicions are based for Sri Lanka, we might be able to make it general(global), and then specialize to other countries. or specialize it to large/small(views) channels, or long/short videos, or channel category wise, or channel view count wise.

Real time data collection(daily) to train and update the ML with latest data. Trending Keywords(among similar channels), personalized video ideas(ideal length range/ ideal title keywords/ ideal description approaches/etc. Competitor/Subscriber analysis, trend alerts, channel audit tool, SEO, keyword research, thumbnail suggestions, video suggestions). All of these should be personalized, Graph view prediction with many data points. Channel analytics, projections(view/monetary), similar channels...

These above features should be thoroughly analysed and considered to make a good plan since the MVP is done by three uni undergrads within 3 months. We can include the harder to implement features in future plans docs. 
Your ambition is fantastic, but for a 3-month project, scope is your most important constraint. You need to define a clear boundary between the Minimum Viable Product (MVP) and future versions.

Explicitly INCLUDED in MVP Scope:

Data Collection: Fetching video metadata (title, duration, category, tags, stats) for a curated list of Sri Lankan channels using the YouTube Data API v3.

Data Storage: Storing this data in a local SQLite database.

Core Models: Training separate regression models (e.g., XGBoost) for Shorts and Long-form videos.

Forecasting: Predicting the view count at three key milestones: 24 hours, 7 days, and 30 days.

User Interface: A simple web page where a user can input a YouTube video URL.

Output: Displaying a graph showing the predicted view curve based on the 3 milestone predictions.

Explicitly EXCLUDED from MVP Scope (for "Future Work" section):

Transcript, audio, and thumbnail image analysis.

Real-time, continuous data collection and model retraining.

SEO tools, keyword research, competitor analysis, and personalized suggestions.

Monetary projections and channel auditing tools.
7. What features will be available in the MVP?
Graph view prediction with many data points.
The "Graph view prediction" feature will be composed of:

Input: A text box where a user pastes the URL of a YouTube video.

Processing: The backend fetches the video's initial metadata (title, duration, category, channel stats).

Prediction: The system feeds these features into the appropriate pre-trained model (Shorts or Long-form) to get view count predictions for 24 hours, 7 days, and 30 days.

Output: The UI displays a line chart. The line starts at the video's current view count and extends into the future, plotting the predicted points at the 24h, 7d, and 30d marks to create a "growth curve."
8. Will the system work only for Sri Lankan creators or have optional generalization?
Intended for sri lankans, but as a business its better to target general/global user. so, there are plans to expnd. (could be channel country wise/ channel category wise/ channel subscriber wise/or channel view count wise)
### 1.3 Definitions, Acronyms, and Abbreviations

9. List all domain-specific terms (e.g., API, RMSE, Prophet, Streamlit, “viewership curve”).
IDK what this is but  API, RMSE, Prophet, Streamlit, “viewership curve" are domain specific terms, yes.

Here’s a starter list you can use and expand upon:

API (Application Programming Interface): A set of rules and protocols that allows different software applications to communicate with each other. We use the YouTube Data API.

ETL (Extract, Transform, Load): The process of collecting data from a source (YouTube), cleaning and transforming it, and loading it into a database.

Feature Engineering: The process of creating new input variables (features) for a model from the raw data (e.g., creating day_of_week from publish_time).

Regression Model: A type of machine learning model that predicts a continuous numerical value, such as view_count.

RMSE (Root Mean Squared Error): A metric used to measure the average magnitude of error in a regression model's predictions.

MAPE (Mean Absolute Percentage Error): A metric that measures prediction accuracy as a percentage, making it easy to interpret.

Viewership Curve: A line graph that plots the cumulative view count of a video over time.

### 1.4 References

10. List any:

* Academic sources (papers/books on forecasting, engagement modeling, etc.)
* Websites/tools (e.g., [YouTube Data API v3](https://developers.google.com/youtube/v3), Streamlit)
* Existing SRS formats used as a reference

### 1.5 Overview

---

## 2. Overall Description

### Product Perspective

12. Is this an independent system or will it integrate with other platforms/tools?
There are plans to extend this service as an extension, possibly on chrome/edge/firefox/etc. And, yes, if we can find any other platform (instead of just internet browsers, we'd be willing to do so)
13. Will it be hosted online or distributed as a desktop app?
Hosted online

### Product Functions

14. What are the high-level modules/features? (e.g., data collection, forecasting, visualization)
All. And also, AI based predictions/suggestions/video planning/etc. as i have explained in a previous step. 

### User Characteristics

15. Who are the target users (e.g., Sri Lankan YouTubers, media companies)?
already discussed
16. What technical expertise is expected of users?
just basic expertise. but maybe we can add a pro version for tech-savvy users(in the future)

### Constraints

17. What are the key limitations? 
YouTube API quota, regional data gaps, performance limits, resource-intensive to calculate multiple projections at the same time, hard to analyse video/audio of a big amount of YT videos first (let alone make predictions for one video)
18. Are there any limitations on tools/libraries used due to OS or deployment choices?
for now not sure, we're trying to make it cross platform(universal) compatible web hosted tool. we use windows and Linux to program. 
The fact that your team uses different operating systems (Windows and Linux) is a perfect reason to use Docker.

Solution: Define your entire application environment in a Dockerfile and a docker-compose.yml file. This includes the exact Python version and all library versions. Everyone on the team then runs the project inside a Docker container. This completely eliminates cross-platform compatibility issues and makes deployment to a cloud server seamless.

### Assumptions and Dependencies

19. What assumptions are being made? 
Trying to make no assumptions, trying to go with the most realistic world scenarios(assumptions will only made when really necessary-when there's no feasible way out)
20. Dependencies on tools/services?
already discussed(might need more)

---

## 3. Specific Requirements

### 3.1 Functionality

21. Describe in detail what the user can do with the tool. 
Already discussed in detail
input a video title and get predictions, compare trends, track videos over time, retention analyser, videolytics, channelytics, opportunity finder, competitor scorecard, SEO and ranking, channel optimization, video and thumbnail, AI features, 
22. What automation features are available? 
already discussed(AI-based suggestions, etc)
scheduled data refreshes, etc.

### 3.2 Usability

23. What are the expectations for ease of use?
fewer buttons, less complex outputs(but can dive into data in a deeper/complex manner if the user needs, it's just the basic look looks simple. (users should be able to do complex things if they need to), more visualizations than text
24. Are there any UI standards you plan to follow?
no, basic good practices that suit this application might be enough. maybe as similar as viewstats, vidiq, vidstats, socialblade, tubebuddy
25. Any requirements for accessibility (e.g., colorblind-friendly)?
not yet

### 3.3 Reliability

26. What is the target system uptime?
24x7
27. How is data integrity ensured?
no idea as for now. but surely we should have plans on that
Data integrity ensures your data is reliable. Here are two simple but effective methods:

Database Constraints: When you design your database schema (e.g., in SQLite or PostgreSQL), use constraints. For example, make sure the video_id is a PRIMARY KEY (must be unique), foreign keys (like channel_id in the videos table) actually exist in the channels table, and important fields like view_count cannot be empty (NOT NULL).

Data Validation Scripts: Before inserting data into your database, your Python script should perform basic checks. For example, ensure that view_count is a non-negative integer and duration is in a valid format.
28. Are any backup or recovery mechanisms needed?
yes, most possibly. but we still dont have plans, which we should create
For a university project, a simple backup strategy is sufficient.

Plan: Set up a scheduled task (a cron job on Linux/macOS or Task Scheduler on Windows) to run once a day. This task should execute a simple script that:

For SQLite: Copies the .db file to a backup folder with the date in the filename (e.g., backup-2025-08-06.db).

For PostgreSQL: Uses the pg_dump command-line utility to create a compressed backup file.

### 3.4 Performance and Security

29. What is the maximum response time expected for forecasts?
1 min(just a random time that came to my mind, we'd have to develop and see ig)
30. How many concurrent users/videos should it support?
as much as possible. start small, and after deployment, slowly progress through.
31. What security measures are planned (e.g., API key protection, user data access control)?
nothing yet, but surely we should implement.
Never, ever commit your API keys to GitHub. Store them in a .env file at the root of your project. Add .env to your .gitignore file. Your Python code will use the python-dotenv library to load these keys as environment variables. This is standard, non-negotiable practice.
32. Will there be any form of authentication or login system?
yeah, a login system would be needed
For the MVP, a simple email and password login system is sufficient. Libraries like Flask-Login can handle most of the heavy lifting (session management, password hashing). Ensure you are hashing passwords using a strong algorithm like bcrypt (Flask-Login can help with this).

### 3.5 Supportability

33. Will the system be maintained by the current team after release?
yes, most probably
34. Will logging and monitoring be part of the system?
yes
35. Will it be open source or have community support?
it's a university project, so i guess it'd be open-source

### 3.6 Design Constraints

36. Are there mandatory libraries, programming languages, or databases to be used?
nope
37. What frameworks (e.g., Streamlit, SQLite3) are chosen and why?
already discussed. open for expanding with other frameworks.
38. Are there compatibility constraints (e.g., must work on Windows, Chrome, etc.)?
universal hosted website

### 3.7 Online Documentation

39. Will there be an integrated help button or user guide?
yes(less priority)
40. Any planned FAQs, tooltips, or walkthroughs?
yes(less priority)

### 3.8 Purchased Components

41. Are any paid APIs, plugins, or tools being used?
still not, but we might need some of them in the future. (we still don't have a clue what we would need) so might wanna plan on that

### 3.9 Interfaces

#### User Interfaces

42. List and describe the pages/modules planned for the UI 
dashboard, input form, trend graph, suggestions, Trending Keywords(among similar channels), personalized video ideas(ideal length range/ ideal title keywords/ ideal description approaches/etc. Competitor/Subscriber analysis, trend alerts, channel audit tool, SEO, keyword research, thumbnail suggestions, video suggestions).
MVP UI Plan:

Login/Register Page: A simple form for user authentication.

Dashboard/Input Page: The main page after login. It should have:

A prominent input field for the user to paste a YouTube video URL.

A "Forecast" button.

A section below to display the results.

Results Display (on the same page):

Displays the video's title and thumbnail.

A large, clear chart showing the predicted viewership curve for the next 7 days.

Key metrics displayed simply (e.g., "Predicted 7-Day Views: 150,000").

All other features (competitor analysis, keyword tools, etc.) should be moved to your "Future Work" documentation.


43. What key controls/fields should each page have?
try to maximize visualisations
dashboard: access to all other tools, login, help,essentials
input: video upload-analysis, analysis without video upload, brainstorm(finetune idea/initial idea creation)
trend graph(output): change timeframe(sensitivity)/ change graph type(according to what's shown in it)
keywords: analytics about each keywords when clicked, keyword filters (by country, type, etc)
suggestions: (channel audit tool, SEO, keyword research, thumbnail suggestions, video suggestions) what trends, what viewers watch most, interesting personalised video ideas(titles/descriptions/content/length)
Competitor/Subscriber analysis: similar channels list of channels, can access each channel to see what videos worked well, what kind videos subscribers are watching
trend alerts: a interface where current trends are shown(can be filtered with video titles, country, thumbnails, content, categories, keywords, hashtags if needed. default: general trending)

#### Hardware Interfaces

44. What are the expected client requirements (RAM, storage, browser)?
browser, ram(for frontend graphs), storage might be needed(not sure), and there might be other requirements that have not been identified yet.

#### Software Interfaces

45. What APIs or external services will the system interact with?
Youtube API v3 for now. and there could be many more that we still haven't identified

#### Communication Interfaces

46. Will it use HTTP/HTTPS, REST, FTP, or WebSockets?
Most probable yes to: HTTPS, REST, FTP, WebSockets
47. Is the system expected to work offline at all?
No

### 3.10 Database Requirements

48. What data needs to be stored?
dataset(which will be updated automatically constantly daily to update the ML model daily), videos, metadata, userdata, logs, session data, security data, cache/cookies(for efficient services), report data, analysis data, ebug data, output data, other data that might be help in improving the model, website, service...
49. What is the expected scale?
depends on the demand(of users and also the upload rate of YT creators)
50. What are the indexing and querying requirements?
currently no idea, wanna plan that too
Database indexes are like an index in a book; they make finding data much faster. For your project, the most critical query will be "get all view count snapshots for a specific video, ordered by time."

Plan: In your Snapshots table, you will have columns like snapshot_id, video_id, timestamp, view_count. You must create a composite index on (video_id, timestamp). This will make generating the historical part of your forecast graphs extremely fast, even with millions of rows.

### 3.11 Legal, Copyright, Licensing

51. Are there copyright or data usage issues with YouTube data?
dont think so as long as the videos are public. no strict rules about using copyrighted content to train AI. as we're not explicitly showing their material to earn money from screening. it's very indirect. 
52. Will users have to agree to terms of use?
still no need for 'terms of use' has arisen. But might wanna consider that as well

Legal: Re-read YouTube's API Terms of Service. The key takeaway is: you can analyze public data, but you cannot aggregate and sell or publicly display the raw data as your own. Your forecasts are derived data, which is generally safer. Add a "Terms of Service" and "Privacy Policy" to your website if you have user logins.

### 3.12 Standards

53. Are there any design/development standards followed (e.g., PEP-8, GDPR, WCAG)?
we might need to do that, but not specified. use a suitable one for this application's SRS
54. Any expected code audit or data protection compliance?
no, might wanna consider. we'll be sharing this on GitHub for development. 

Coding: Adopt the PEP-8 style guide for all Python code. Use a tool like flake8 or black to automatically enforce it.

Version Control: Use a Gitflow-like branching strategy (e.g., a main branch, a develop branch, and feature branches for each task). This prevents conflicts and keeps your main branch stable. Write clear, concise commit messages.

---

## 4. Supporting Information

55. Will there be any appendices (e.g., diagrams, data samples)?
yes, if so, its better(don't know what they should be though)
56. Any system diagrams, user flowcharts, or architecture sketches planned?
yes. system diagrams, user flowcharts, gantt charts and architecture sketches
57. Will screenshots or mockups be added later?
yes.


====Software Architecture Document====
## 🔹 1. Introduction

### 1.1 Purpose

* Who are the **intended readers** of this document (developers, testers, stakeholders, etc.)?
developers, testers, stakeholders, lecturers, mentors, teaching assistants
* Is this document expected to **guide future enhancements**, or only cover the current version?
expected to guide future enhancements

### 1.2 Scope

* What **software and hardware components** are affected by this architecture?
not sure for now. ram for sure, gpu for visualizations possibly? and cpu. wanna plan on that
The architecture will primarily involve:

Backend Server: This is where your data processing, model predictions, and API will run. It will be CPU-intensive during data processing and model inference (for XGBoost/Random Forest) and will require sufficient RAM to hold your dataset and model in memory.

Database Server: This component will handle data storage and retrieval. It's primarily sensitive to Disk I/O speed (how fast it can read/write data) and RAM for caching queries.

Client-Side (User's PC): This will run the web browser. The primary resource used will be RAM for rendering the JavaScript-based visualizations (graphs). A GPU is generally not required for rendering the 2D charts you're planning.
* Are **external systems/APIs** (e.g., YouTube Data API, Google Trends API) part of the scope?
yes. YouTube Data API. would wanna formulate a method to use other APIs too. cause we're sure that we would need them, but don't know what we need and when we need them

### 1.3 Definitions, Acronyms, and Abbreviations

* Can you list **technical terms or abbreviations** used in the system (e.g., KPI, API, ML, UI, YT)?
obvious from this(and we can include possible ones that we'd use in the future)

### 1.4 References

* List any **relevant textbooks, research papers, tools**, or websites you want cited.
* What tools will you use to draw the diagrams? (e.g., draw\.io, Lucidchart, StarUML, etc.)

### 1.5 Overview

* Summarize how this document is **structured** for the reader.

---

## 🔹 2. Architectural Representation

* Which architectural views do you plan to use from these: **Use-case**, **Logical**, **Process**, **Deployment**, **Implementation**, **Data View**?
have no idea. more the better. and also, there might be ones that are must or less necessary according to our project. before creating these diagrams, we must identify all the entities and functionalities, etc of the system.
You're right that you need to identify entities first, but you can plan which views to create. For a project of this scale, focusing on a few key views is most effective. I recommend:

Logical View: Shows how the system's functionality is broken down into code. This is where you'll have diagrams of your main modules (Data Collector, Preprocessor, Model, API) and how they relate.

Process View: Shows how the system runs. A sequence diagram for a "User Forecast Request" would be perfect here. It shows the flow: UI -> Backend API -> Model -> Database -> UI.

Deployment View: Shows the physical layout. This would be a simple diagram showing the User's Browser, your Cloud Server (containing the Web App and ML Model), and the Database.
* Are you adopting any **architecture style or pattern** (e.g., MVC, layered, microservices)?
no idea as per now, but if there's a preferred one for our system, then we would use it. 
A Layered Architecture (also known as N-Tier Architecture) is the perfect fit for this project. It's a standard, robust pattern that separates concerns cleanly.

Presentation Layer (Frontend): The web interface your user sees. (e.g., Streamlit or HTML/CSS/JS).

Business Logic Layer (Backend): The "brains" of your application. This is your Flask/Python code that handles requests, calls the model, and processes data.

Data Access Layer: A set of functions or a class responsible for all communication with your database (reading and writing data).

Data Source: The PostgreSQL/SQLite database itself.

This pattern makes your system easier to build, test, and maintain because each layer has a distinct responsibility. Microservices would be overly complex for this project.


---

## 🔹 3. Architectural Goals and Constraints

* What are your key **non-functional requirements**?
we can analyse the needs of the system(which are explicitly mentioned) and easily come up with these(a few that comes to my mind are as follows, not might be the complete list)
accessibility/compatibility: should be accessible via any OS, device at any time using an active internet connection and a browser.
availability: should be available 24x7, all system failures should be handled gracefully
deployability: should be hosted with use of HTTPS, FTP, WebSockets
Documentation: Yes, all documents that are needed are listed above. 1. Project Feasibility Document, 2. Project Schedule (Gannt Chart)), Mentor meetup 1, Project Idea Submission, Project Proposal Submission, (1. Project Feasibility Document, 2. Project Schedule (Gannt Chart)),Work on the system requirements, specification and design, (3. System Requirement Specification, 4. System Architecture and Design), Mentor meetup 2, Development Iteration 1, 5. Midevaluation, Development Iteration 2, 6. Testing & Evaluation Document, Mentor meetup 3, 7. Final Evaluation, 8. Final Product Resources submission, 9. Final Report Submission
Efficiency: Should use cloud, backend, frontend and user device resources efficiently to optimize the performance of the system. 
Extensibility: All the services should be extensible from the minimum viable product to the functionalities we discussed above.
Maintainability: Every part of the system should be easily maintainable and fixable. Should be easily able to update the system with any upgrades we find necessary.
Performance: system should perform well accurately and fast with the minimum possible weight on servers as well as user device. 
Recoverability: Multiple DBs, user side cookie/cache, can be used to safeguard data, to make them recoverable. 
Reliability: The system should provide super accurate predictions no matter what user type. 
Responsiveness: All buttons should work, and quickly within a few milliseconds, they should start doing what they're intended to. The results, calculations, visualizations shouldbe responsive and quick.
Scalability: should be scalable upto hundreds of thousands of concurrent users.(one might be using AI tools, one might be using predictor tools, one might be using graph tools, etc)
Robustness: Resistant to bugs, hacking, and multiple users at once, etc.
Safety: Database data should be strictly protected.
Testabiliy: Each component of the system should be thoroughly testable
Usability: the usage and UI should be very intuitive and easy

* Do you have **constraints** such as:

  * Required use of certain tools or frameworks?: no
  * Platform/language restrictions?: no
  * Deadline pressure?: yes
  * Limited hardware?: yes(currently we have windows 11 and ubuntu 2024 laptops, hardware are at 16GB RAM, i7/R7 processor, rtx gpu,  2 windows + 1 ubuntu)

---

## 🔹 4. Use-Case View

### General

* Provide at least **5 primary use cases** of the system.
Forecast YouTube Views, Visualize Trend Data, Upload Channel Info, etc. when we look at the functionalities, they explicitly mention the usecases.
For each main use case, please provide:

### 4.1 Use-Case Realizations (for each selected use case): Need to be planned for each

* **Use case name**:
* **Actor(s)**:
* **Description**:
* **Preconditions**:
* **Main Flow** (step-by-step actions):
* **Successful Postcondition**:
* **Fail Postcondition**:
* **Extensions/Alternative Flows**:

---

## 🔹 5. Logical View

### 5.1 Overview

* What are the **main subsystems or modules** in your software
Some that comes to mind are: Data Collection, Forecast Engine, Trend Analysis UI, schedulers/automators, model training, AI interactions/suggestions, visualizers, etc. (explicit and obvious from previous discussion)

### 5.2 Architecturally Significant Design Packages

* For each major subsystem, what are the **key classes**, **their purposes**, and **relationships**?
These should be planned.
* What design pattern(s) (if any) are used (e.g., Singleton, Factory, MVC)?
These should be planned.
* Do you want to include service classes, data access classes, utility classes?
These should be planned.

---

## 🔹 6. Process View

* What are the **main processes** and **threads** involved?
These should be planned. Some that comes to my mind are: Forecast Engine, Trend Analysis UI, schedulers/automators, model training, AI interactions/suggestions, visualizers, etc.
* How do components communicate (synchronous API calls? async messaging? file-based transfer)?
This would need some proper analysis and planning as each component would have different needs.
* Will any component run **in parallel** or as a **background process**?
Most probably, but we have to figure out yet
* Describe the key **sequence diagrams** you want to include (e.g., “User Forecast Request Flow”).
Need to be discussed/planned after initial planning is concluded

---

## 🔹 7. Deployment View

* What is your **deployment environment** (e.g., local machine, cloud platform, university server)?
developed on local machines using GitHub and deployed on cloud
* Describe the **hardware setup** (e.g., frontend server, backend server, DB instance).
we just have three laptops for ourselves. other further things need to be discussed.
* Are any parts of the system **distributed**?
i dont even know what this means
"Distributed" means that different parts of the system run on separate physical or virtual machines and communicate over a network.

For your MVP: Your system will not be distributed. It will be a monolithic application, where your web server (Flask), machine learning model, and data processing scripts all run on the same cloud server. This is simpler and cheaper to manage.

Future aistribution: A future, larger-scale version could be distributed (e.g., having a separate server just for running ML models), but that is not a concern for your current scope.


* Will the system use a **web browser**, **mobile app**, or desktop UI?
web browser

---

## 🔹 8. Implementation View

### 8.1 Overview

* What is your planned **layering strategy** (e.g., UI → Controller → Service → Data Access)?
still nothing, Need to be discussed/planned along with initial planning. there might be a specialized/optimized way to implement layering.
* Which technologies are assigned to which layers (e.g., Streamlit frontend, Python logic, SQLite)?
still nothing, Need to be discussed/planned along with initial planning. there might be a specialized/optimized way to implement layering.
This directly relates to the architectural pattern. Here is a concrete plan based on the Layered Architecture:

Layering Strategy:

Presentation Layer (UI): Responsible for rendering web pages and visualizations.

Application Layer (API): Responsible for handling incoming HTTP requests (e.g., /predict).

Domain/Logic Layer (Core Logic): Contains the Python modules for feature engineering, model prediction, and data analysis.

Data Access Layer (DAL): Contains all the SQL queries and database connection logic.

Technology per Layer:

Presentation: Streamlit or HTML/CSS/JavaScript with Chart.js.

Application: Flask to create the REST API endpoints.

Domain/Logic: Pandas, Scikit-learn, XGBoost.

Data Access: SQLAlchemy (an ORM that works well with Flask) or the sqlite3/psycopg2 libraries directly.

Coding Conventions: Officially adopt PEP-8 for all Python code. Use a linter like flake8 in your code editor to automatically check for compliance. This will make your code much more readable and consistent.

### 8.2 Layers

* Name each layer and list the **key components** or **subsystems**.
still nothing, Need to be discussed/planned along with initial planning. there might be a specialized/optimized way to implement layering.
* Do you follow any **coding conventions** or **framework rules**?
still nothing, Need to be discussed/planned along with initial planning. there might be a specialized/optimized way to implement layering.

---

## 🔹 9. Data View (Optional)

* Will you use a **database**? If yes:
Yes
  * What kind? (e.g., SQLite, Firebase, PostgreSQL)
SQLite (mostly) or postgre
  * What are the main **tables or collections**?
i don't even know what this is
"Tables" are how data is organized in a relational database like SQLite or PostgreSQL, similar to spreadsheets. Based on your project needs, here is a starting database schema you can use:

channels Table:

channel_id (Primary Key, Text)

channel_name (Text)

subscriber_count (Integer)

channel_video_count (Integer)

videos Table:

video_id (Primary Key, Text)

channel_id (Foreign Key to channels.channel_id)

title (Text)

published_at (Timestamp)

duration_seconds (Integer)

category_id (Integer)

is_short (Boolean)

snapshots Table:

snapshot_id (Primary Key, Auto-incrementing Integer)

video_id (Foreign Key to videos.video_id, Indexed)

timestamp (Timestamp, Indexed)

view_count (Big Integer)

like_count (Integer)

comment_count (Integer)

tags Table & video_tags Junction Table (for many-to-many relationship)

You can add these later if you decide to analyze tags in detail.

This structure is a solid foundation for storing all the data you need.
  * Provide any **ER diagrams** or **schema overviews**.
This should be planned after properly analyzing and identifying the system components, entities, relations, etc.
* Are you storing **raw API data**, **processed stats**, or **user-generated input**?
yes, all three might be needed for different usage cases. although we still don't know what it is, we're sure that some usage need would arise.

---

## 🔹 10. Size and Performance

* What’s the expected **data volume** (e.g., number of videos, views per month)?
i don't know, we just predict how many views a video can get in a certain time, and also system might get popular with time, and this question doesn't make sense to me
* What are your **performance expectations** (e.g., forecast returned in <3s)?
* Are there any **limits** from APIs or hosting services that impact performance?
yes could be, currently YT API. we should make plans to manage all these possibile limitations

---

## 🔹 11. Quality

* What **quality attributes** are most important? (e.g., scalability, usability, reliability, maintainability?)
reliability, performance, robustness, efficiency, compatibility, usability, responsiveness, deployability, availability, maintainability, extensibility, scalability, testability, documentation
* How does your design ensure:

  * **Security** (especially when working with API keys)?: not planned
  * **Privacy** (if user or creator data is sensitive)?: not planned
Even for a university project, basic security is crucial.

Security Plan:

Protect API Keys: Store all secret keys (YouTube API, database passwords) in a .env file. Add .env to your .gitignore file to prevent them from ever being uploaded to GitHub.

Password Hashing: When you implement the login system, use a library like werkzeug.security (which comes with Flask) to hash user passwords with generate_password_hash and check them with check_password_hash. Never store plain-text passwords.

Privacy Plan:

Create a simple "Privacy Policy" page on your website.

State clearly that you collect user emails for authentication purposes only and will not share them.

State that you are using the YouTube API and link to Google's Privacy Policy. This is required by the YouTube API Terms of Service.
  * **Portability** (can it run on other platforms)?: multiple browsers, yes. other platforms, yes we have plans to expand, but not in the MVP.
  * **Extensibility** (can you add TikTok or Instagram later)?: dont think so

---

## 🔹 12. References

* Any books, websites, or articles you want cited?
  (E.g., “Time Series Forecasting with Python,” “YouTube API v3 Documentation,” etc.)
* Include links/tools used to create diagrams.


========Feasibility Report=======
## ✅ Section 1: Introduction

### 1.1 Overview of the Project

* What are the **core products or services** the system will offer?
already discussed
* What **problems** does the system aim to solve for the user (YouTube creators or analysts)?
the unailability of tools that are refined and fine tuned like this. there are analytics tools, but they lack the capability to predict a video's virality factor. (based on region, category, length, content, etc.)
* How does it **benefit the client or users** (e.g., better content strategy, saving time, increasing reach)?
they can get an idea before uploading the video, plan better, use tools like optimal length/title/description/content/hashtags to plan their videos beforehand, refine their videos using suggestions
* Is there any **competitive edge** the project offers over manual forecasting or existing systems?
Yes, as mentioned above there are no many systems that do this. manual forecasting could be good but when we train the data with 6 consecutive months each for a few years, we'd be able to predict the algorithm better. there might be more advantages too, but this is what i could think of now.
This is a good start. You can make your competitive edge much more specific and compelling by highlighting these points:

Hyper-Local Focus: Existing global tools (like VidIQ, TubeBuddy) use massive, generalized datasets. Your competitive edge is a model trained specifically on Sri Lankan viewership data. This allows it to capture local language nuances, cultural trends, and prime viewing times unique to Sri Lanka, which global models miss.

Predictive vs. Reactive: Most tools provide historical analytics (what happened). Your core feature is predictive analytics (what will likely happen). This shifts the value from reporting to strategic planning.

Holistic Feature Analysis: You're not just looking at one factor. Your model will be trained on the combined influence of title, category, publish time, channel authority, and duration, providing a more sophisticated forecast than a human can do by gut feeling alone.

---

### 1.2 Objectives of the Project

* List the **primary goals** of the system
automating predictions, visualizing data, optimizing publishing time, and other mentioned objectives(that were mentioned above)
* Do you aim to **assist content creators**, **analyze viewer behavior**, or both?
Both
* Are there any **secondary objectives**, such as creating a dataset or publishing research?
Yes, creating a dataset, publishing research and publishing this product are all three objectives 

---

### 1.3 The Need for the Project

* Why do Sri Lankan creators need a **localized** YouTube forecasting tool?
there are no local YT datasets, nor local tools in Sri Lanka
* Are there any **shortcomings in existing tools** (e.g., lack of local relevance, inaccessibility, too technical)?
Yes. Lack of relevance and inaccessibility to some features that we are going to offer
* Is there any **client**, stakeholder, or community expressing the demand for this?
yes, YT is in demand. 
* Will this help **niche creators**, marketing firms, or businesses trying to enter YouTube?
yes

---

### 1.4 Overview of Existing Systems and Technologies

* What are some **existing systems/tools** that offer view forecasting or YouTube analytics?
TubeBuddy, Vidooly, SocialBlade, Google Trends, VidIQ, viewstats
* What are their **limitations**, especially for the **Sri Lankan market**?
No region wise analysis(socialblade has region wise ranking only), google trends is too hard to acces, viewstats provide innacurate data/predictions, and we aim to provide maximum possible accuracy using data science and statistics that we can derive from YT data
* What **software development tools/libraries/databases** are being considered? (List both frontend and backend)
Wanna formulate the project and come up with the most suitable ones, the ML part would be python
* Are there any **emerging technologies** you’re planning to experiment with? (e.g., LLMs, semantic expansion, graph algorithms)
don't think so. (do they really fit here is a question that we'd have to consider)
You are correct to be cautious for the MVP. Sticking to established ML models like XGBoost is the right call. However, you can show foresight in your report by mentioning how emerging tech could be used in the future:

LLMs (Large Language Models): For a "V2.0" of ViewTrendSL, an LLM could be used for advanced feature creation, such as analyzing the sentiment of a video title and description or even generating optimized title suggestions for users.

Graph Algorithms: Could be used in the future to analyze the relationships between channels (e.g., who collaborates with whom) to see if that impacts viewership, but this is outside the MVP scope.

---

### 1.5 Scope of the Project

* What are the **user roles** in the system? 
Creator(simple-user), analyst(complex-pro user with complex tech capabilities), admin
* For each user role, list **core functionalities** (e.g., run forecast, view trends, export data).
admin: manage other users, 
creators: basic forecasting
analyst: foreacasting + complex usage. coding+etc.
* Are there any **limitations** in terms of geographical scope, platform support, or language?
no geographical limitations, but only English currently. 

---

### 1.6 Deliverables

* What will be the **final product**? (e.g., web-based system, dashboard, downloadable dataset)
web-based system, downloadable dataset, sourcecode(if open source), etc.
* Will there be a **GUI**? If yes, what are its features?
yes. features to provide the user with the required functionalities.
* Will you deliver **documentation**, a research paper, or developer tools alongside the system?
yes

---

## ✅ Section 2: Feasibility Study

### 2.1 Financial Feasibility

* What **budget constraints** are present, if any?
not much budget. since this is a university project done by 3 students within 3 months. 
* Are any **paid APIs, tools, or hosting services** required?
might be, but have not identified yet. the requirements might be of help in finding/understanding this need
* Will you be using **free-tier services** (e.g., Streamlit Community Cloud, SQLite, HuggingFace APIs)?
yes, when needed
* What is the **estimated cost** breakdown (if applicable):
not yet calculated

  * Data storage
  * API quota or upgrade
  * Domain/hosting
  * Dev time (if this was a billable service)
(should analyse it alongside the project plan)
A feasibility study should include a concrete, even if estimated, budget. For a student project, you can frame this as a "Zero-Cost MVP" plan.

Estimated Cost Breakdown (MVP):

Data Storage: $0. Use SQLite for local development. For deployment, use the free tier of a service like ElephantSQL or Supabase, which offers a generous PostgreSQL database.

API Quota: $0. Utilize the standard free quota from the YouTube Data API. Manage it efficiently by rotating the three team members' keys and caching results.

Domain/Hosting: $0. Deploy the application using a free-tier platform like Heroku, Vercel, or PythonAnywhere. They provide a free subdomain (e.g., viewtrendsl.herokuapp.com).

Dev Time: Not a monetary cost, but estimate it in hours. For a 3-person team over 12 weeks, a rough estimate could be (10 hours/week/person) * 3 people * 12 weeks = 360 person-hours.

This shows you've considered the costs and have a viable plan to deliver the project with zero financial outlay.

---

### 2.2 Technical Feasibility

* What **languages, libraries, frameworks, and APIs** are you planning to use?
already mentioned(frameworks+libraries). APIs:YT data, YT trends, YT analytics, etc as the need arises. languages(python, etc: as the need arises)
* Is the architecture **centralized**, **modular**, or **distributed**?
most probably centralized. or could be distributed if this becomes open source?
Let's clarify these terms for your document:

Architecture: Your MVP will have a Centralized (or Monolithic) Architecture. This means the entire application (web server, backend logic, model prediction) runs as a single process on one server. This is the simplest and most appropriate choice.

Design: Within that centralized architecture, you should use a Modular Design. This means your code is broken into logical components (data collection, feature engineering, API endpoints, etc.), making it clean and maintainable.

"Distributed" refers to running different components on different servers (microservices), which is overly complex for now. "Open source" is about licensing, not architecture.
* Is there any **expected technical difficulty** in:

  * Collecting localized YouTube data?
Yes. The YT API doesn't provide them explicitly. we have to use our APIs inefficiently to find and verify sri lankan(location-wise) data. There could be more. 
  * Forecasting with limited Sri Lankan video metadata?
Yes, we need to collect our data
  * Rendering complex visualizations or graphs?
yes. we try to maximise easy-to-understand visualizations. but they don't need to be complex(say, we don't need 3d visualizations), we just need simple ones
* Will the solution support **scalability** (e.g., from 100 to 10,000 videos)?
yes, it should

---

### 2.3 Resource and Time Feasibility

* What are the **hardware/software requirements** for development and deployment?
(currently not planned, should come up with stuff according to the project ideas)
  * Dev machines
  * Hosting environments
  * GPU/CPU needs (if any)
* Do you expect the project to be completed within the **course duration** or do you anticipate **extending it** as a long-term solution?
MVP should be completed within 3 months and we have plans to expand it.
* How many **active contributors** are involved and what are their roles?
3. already mentioned
* What is your **estimated timeline per phase** (data collection, modeling, interface, testing, presentation)?
no timeline, should come up with one
A timeline (Gantt chart) is a critical deliverable. Here is a sample 12-week plan you can adapt:

Weeks 1-2: Planning & Setup

Finalize SRS and Architecture documents.

Set up GitHub repository, Docker environment, and API keys.

Create initial database schema.

Weeks 2-4: Data Collection & EDA

Build and run data collection scripts.

Clean the initial dataset.

Perform Exploratory Data Analysis (EDA) to find initial insights.

Weeks 5-7: Model Development & Training (Iteration 1)

Feature Engineering.

Train baseline models (e.g., Linear Regression, Random Forest).

Train primary models (XGBoost for Shorts & Long-form).

Evaluate and select the best models.

Weeks 6-9: Backend & Frontend Development (Parallel)

Develop the Flask API to serve the model.

Develop the Streamlit/HTML user interface.

Integrate frontend with the backend API.

Week 10: Testing & Refinement

End-to-end system testing.

Bug fixing and performance tuning (e.g., implementing caching).

Weeks 11-12: Finalization

Deploy the application to a cloud provider.

Finalize the project report, presentation, and all documentation.

Prepare for the final evaluation.
---

### 2.4 Risk Feasibility

* What **data-related risks** are possible?

  * API limits
  * Incomplete or biased metadata
* What **technical risks** are expected?

  * Overfitting of forecasting models
  * Bad model performance due to niche data
  * Limited Sri Lanka-specific content on YouTube
* Any **deployment/maintenance risks**?

  * Hosting limitations
  * Downtime
* What **mitigation strategies** will you adopt? (e.g., caching, data cleaning, backup models)
For every risk, you need a plan.

Risk: API limits halting data collection.

Mitigation: Use efficient API endpoints, implement caching for API calls, and rotate the team's 3 API keys to triple the daily quota.

Risk: Overfitting the model due to niche data.

Mitigation: Use cross-validation during training. Employ regularization techniques in the model (XGBoost has built-in parameters for this). Focus on strong feature engineering rather than overly complex models.

Risk: Bad model performance.

Mitigation: Start with a simple baseline model. If your complex model can't beat a simple average, you know you have a problem. Focus heavily on cleaning the data and creating meaningful features, as this often yields better results than complex model tuning.

Risk: Hosting limitations or downtime.

Mitigation: Use a reputable cloud provider with a good free tier (e.g., Heroku). Implement a free monitoring service like UptimeRobot to get email alerts if your site goes down.

---

### 2.5 Social/Legal Feasibility

* Are there any **legal constraints** on using YouTube data? (e.g., API Terms of Use, Data Privacy)
* Are you ensuring **compliance** with Google’s API quota, content policies, or user data restrictions?
* Could the system unintentionally be used for **manipulation or spam**?
* Are there **social impacts** of democratizing forecast data (e.g., equalizing advantage between big and small creators)?
Legal Constraints: Your use of public data for analysis and forecasting is generally considered transformative and falls under fair use, but you must adhere to the YouTube API Terms of Service. Add a disclaimer to your site stating you are not affiliated with YouTube and link to their ToS.

Compliance: To ensure compliance, log all your API calls to monitor quota usage. Do not store any PII from video comments or user data without explicit consent and a privacy policy.

Manipulation/Spam: Acknowledge this risk. The tool's purpose is strategic guidance. You can mitigate misuse by requiring user logins (which adds a barrier to bots) and potentially rate-limiting prediction requests per user.

Social Impact: Frame this as a positive. Your tool democratizes data science, giving smaller Sri Lankan creators access to insights that were previously only available to large media companies with dedicated analyst teams, thus leveling the playing field.

---

## ✅ Section 3: Considerations

* Which of these are **most important** to the success of your system? Rank them:

  4. Performance
  1. Accuracy
  3. Usability / Ease of use
  2. Explainability of forecasts
  5. Visualization
  6. Platform Independence
  8. Localization
  7. Integration with third-party tools
* Is the system expected to evolve (e.g., include TikTok or Instagram in future)?
no
* Do you expect **mobile access** or is it primarily desktop/web?
primary:desktop
---

## ✅ Section 4: References

* Which **academic papers, tool documentation, YouTube policies, or blogs** will be referenced?
* Which **ML algorithms**, if any, are drawn from textbooks or journal papers?
* List any **URLs, documentation, or whitepapers** you’ll include (can be tentative).


=======PROJECT SCHEDULE========

🔰 General Preferences

G1. Preferred Process Model

Do you want the schedule to be based on:

🧱 Traditional SDLC (Preliminary Analysis → Requirement → Design → Dev → Testing → Deployment)

🔁 Rational Unified Process (Inception → Elaboration → Construction → Transition)

Should the schedule include overlapping tasks (parallel activities), or do you prefer a linear task model?
Recommendation: A Hybrid Model. You will follow a phased approach similar to the traditional SDLC for your documentation and major milestones (Reqs -> Design -> Dev -> Test). However, within the Development/Construction phase, you should work iteratively and in parallel. For example, the backend API and frontend UI can be developed simultaneously once the API contract (how they talk to each other) is defined. This gives you the structure required for university reporting, with the flexibility needed for software development.

🕓 Timeline Constraints

T1. Course Timeline

Project Period (Example): a 10-week time, August 24th, 2025 to November 1st, 2025.

Major Academic Milestones (Example Mapping):

Project Idea Submission: Week 2 (Completed)

Project Proposal Submission: Week 2 (Completed)

1. Project Feasibility Document & 2. Project Schedule (Gantt Chart): Week 3

3. System Requirement Specification (SRS) & 4. System Architecture and Design (SAD): Week 3

Mentor Meetup 1, 2, 3: Approx. Weeks 1, 4, 9

5. Mid-evaluation (Prototype Demo): Week 6

6. Testing & Evaluation Document: Week 8

7. Final Evaluation (Live Demo): Week 10

8. Final Product Resources & 9. Final Report Submission: Week 10

👥 Team & Roles

R1. Members

List the members involved and what role each one plays:

Senevirathne S.M.P.U.: Data Lead. Handles all data collection, initial data cleaning, and exploratory data analysis (EDA). He is the expert on the source data.

Sanjula N.G.K.: Backend & Model Lead. Handles feature engineering, model training/evaluation, building the backend API with Flask, and managing the database schema.

Shaamma M.S.: Frontend & Documentation Lead. Handles building the user interface (UI) with Streamlit/HTML, creating data visualizations, and taking the lead on writing and formatting all project documents (SRS, SAD, Final Report, Presentation).

While tasks are assigned, the whole team should collaborate and review each other's work, especially during the design and modeling phases.

Will all tasks be done collectively, or will certain tasks be assigned to specific members?

📁 Project Phases and Subtasks

P1. Inception / Preliminary Analysis

What activities were/are involved in the initial planning phase?

Ex: defining goals, identifying stakeholders, feasibility discussion
Brainstorming project ideas and scope.

Defining the core problem: lack of localized viewership forecasting for Sri Lanka.

Identifying stakeholders: Sri Lankan content creators, digital marketers, and university mentors/evaluators.

Conducting initial feasibility discussions.

What tasks were done before project approval (e.g., proposal writing, mentor consultation)?
Initial consultation with the project mentor.

Writing and submitting the Project Idea and Project Proposal documents.

Beginning research on existing tools (VidIQ, SocialBlade) and the YouTube Data API.

P2. Requirements Gathering

What specific sub-activities did you do (or plan) for:

Gathering system requirements: Formalizing the MVP scope (predicting views at 24h, 7d, 30d for SL channels) and future features.

Researching YouTube API / forecasting models: Analyzing API quota costs for different endpoints and researching the suitability of XGBoost vs. time-series models for this specific problem.

Interviewing or surveying YouTube creators (if any): [SUGGESTION] Conduct a brief 5-question survey with 5-10 local creators to validate pain points and desired features.

Writing SRS document: Compiling all functional and non-functional requirements into the formal SRS document.

P3. System Design

What design activities will you include?

Creating UI/UX wireframes or mockups for the dashboard and prediction results page.

Designing the system architecture using a Layered Architecture pattern.

Creating a detailed Data Flow Diagram showing how data moves from the YouTube API to the database, to the model, and finally to the user.

Designing the Database Schema with an Entity-Relationship Diagram (ERD).

Writing the Software Architecture and Design (SAD) document.


P4. Implementation / Construction

Break down the development phase into actionable, verb-based subtasks. For example:

Data Pipeline:

Implement Python script using google-api-python-client to fetch channel IDs from a curated list.

Develop a script to retrieve video metadata (title, duration, tags, category) and statistics (views, likes) for each video.

Write a data transformation script using pandas to clean data, convert types (e.g., ISO 8601 duration to seconds), and store it in a structured CSV or directly into the database.

Set up the initial SQLite database schema.

Machine Learning Model:

Engineer features from raw data (e.g., publish_hour, day_of_week, title_length).

Split the dataset into training, validation, and test sets (70/15/15).

Train separate XGBoost models for "Shorts" and "Long-form" videos.

Evaluate models against the test set using MAPE and RMSE metrics.

Serialize the trained models and preprocessing pipelines using joblib.

Backend (API):

Initialize a Flask project with a clear folder structure.

Create API endpoints: /predict (POST), /register (POST), /login (POST).

Implement logic in the /predict endpoint to load the correct model (.joblib file), preprocess input data, and return a JSON forecast.

Integrate password hashing (bcrypt) for user authentication.

Frontend (UI):

Set up a Streamlit or basic HTML/CSS/JS project.

Build the main user dashboard with an input form for a YouTube URL.

Use JavaScript's fetch API to call your backend /predict endpoint.

Integrate a charting library (like Plotly or Chart.js) to render the forecast graph from the API response.

Will implementation be done in modules or as a monolithic system?
The implementation will be modular (e.g., data_collector.py, model_trainer.py, api.py are separate modules), but the deployment will be a monolithic system (a single application running on one server), which is appropriate for the MVP.

P5. Testing and Integration

What types of testing will be done?

Unit testing: For small, pure functions, such as data cleaning utilities (e.g., a function that converts "PT1M30S" to 90 seconds) and feature extraction logic.

Model accuracy/graph evaluation: Evaluating the trained models against the held-out test set using MAPE and RMSE.

GUI/usability testing: Informal testing where team members and a few friends try to use the application to see if it's intuitive.

Integration testing: Verifying that the frontend correctly sends requests to the backend, the backend correctly processes them, and the frontend displays the result.

Will testing be ongoing with implementation or done later?

Testing will be ongoing. Unit tests should be written as features are developed. A dedicated testing phase (Week 7) will focus on integration and end-to-end testing.

Will you write a Test Plan document?

Yes, the Testing & Evaluation Document is a required deliverable for Week 8.

P6. Deployment / Transition

How will you deploy the system?

Web deployment on a free-tier cloud platform like Heroku or PythonAnywhere using Docker for containerization.

Do you need to train users or prepare deployment docs?

No user training is needed. Deployment documentation will consist of a comprehensive README.md file in the GitHub repository and the Dockerfile itself.

Will the final system be demonstrated live?
Yes, a live demonstration is required for the final evaluation.

Do you plan any user acceptance testing?
Yes, informal User Acceptance Testing (UAT) will be conducted by having the project mentor and a few classmates use the live deployed application and provide feedback.

P7. Documentation & Reports

List all documents you need to prepare and submit:

Project Proposal

Feasibility Report

System Requirements Specification (SRS)

Software Architecture and Design (SAD)

Project Schedule (Gantt Chart)

Testing & Evaluation Document

Final Report

Research Paper (Secondary Objective)

A simple User Guide (can be part of the README or Final Report).

Do you want document tasks to be separate activities or embedded under each phase?
Documentation tasks should be embedded. The SRS is the final output of the Requirements phase, the SAD is the output of the Design phase, etc. This makes the work manageable.

🔁 Review and Iteration

Team Meetings: Twice weekly (e.g., Monday to plan the week, Friday to review progress).

Mentor Meetings: Every two weeks, aligned with your university's schedule.

Review your progress internally as a team?

Do you want to include:

“Revise Model”

“Refine UI”

“Conduct Mid-project Review”

“Fix bugs based on testing”
Yes, the schedule should explicitly include blocks of time for:

"Fix bugs from testing" (Week 8)

"Refine UI based on feedback" (After Mid-evaluation in Week 5)

"Conduct Mid-project Review" (Week 5)


🛠 Tools

What tools are you using or planning to use for:

Gantt chart creation: Google Sheets, TeamGantt, or similar online tools.

Development: VS Code, Python, Flask, Docker, Git & GitHub.

Data visualization: Matplotlib & Seaborn for EDA; Plotly or Chart.js for the interactive dashboard.

Forecast modeling: Pandas, NumPy, Scikit-learn, XGBoost.

Version control: Git & GitHub.

🏁 Final Outputs

What is the final deliverable for submission?

A working, deployed web application.

A complete GitHub repository with well-documented code.

All required project reports in PDF format.

A final presentation slide deck.

A short (2-3 minute) demonstration video is highly recommended as a backup for the live demo.

What’s the planned date range for:

Demo preparation & Presentation practice: Week 9.

Final testing: Week 8.

Report finalization: Weeks 8-9.

🧾 Optional

Would you like the Gantt Chart to:

Be visually structured by phase color: Yes, this is best practice. (e.g., Blue for Planning, Orange for Data, Green for Development, Purple for Testing).

Highlight milestones: Yes, milestones like "Proposal Due" and "Final Demo" should be clearly marked.

A text-based task breakdown for Moodle upload: this format is ideal for easy copying and pasting into university submission systems or project management tools


===🧠 MASTER QUESTION SET FOR “VIEWTRENDSL”====
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

