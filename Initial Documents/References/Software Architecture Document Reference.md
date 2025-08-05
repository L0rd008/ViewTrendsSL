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
