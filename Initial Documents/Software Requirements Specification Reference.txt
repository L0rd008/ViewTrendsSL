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
