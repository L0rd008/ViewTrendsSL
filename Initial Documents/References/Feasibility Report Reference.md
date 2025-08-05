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

