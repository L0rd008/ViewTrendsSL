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