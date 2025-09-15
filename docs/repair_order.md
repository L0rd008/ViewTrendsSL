### ## Phase 1: Foundation Layer (Data Storage & Configuration)

This phase establishes the project's backbone: its configuration and database structure. Everything else depends on this.

1.  **Environment & Configuration Files**
    * `.env.example` & `.env`
    * `requirements.txt`, `requirements-dev.txt`, `requirements-prod.txt`
    * `pyproject.toml`, `pytest.ini`
    * `config/__init__.py` and all modules within `config/`
2.  **Database Foundation**
    * `src/data_access/database/base.py` (SQLAlchemy base)
    * `src/data_access/database/connection.py` (Database connections)
    * `src/data_access/database/session.py` (Session management)
    * `scripts/database/setup/init_database.py` (Database initialization)
3.  **Data Models** (Review in this order to respect dependencies)
    * `src/data_access/models/__init__.py`
    * `src/data_access/models/user.py` (Independent table)
    * `src/data_access/models/channel.py` (Independent table)
    * `src/data_access/models/video.py` (Depends on `channel`)
    * `src/data_access/models/snapshot.py` (Depends on `video`)
    * `src/data_access/models/tag.py` (Many-to-many with `video`)

> **Action/Tip:** 📝 Your immediate goal is to get a successful database connection. First, **create your `.env` file** from the example and fill in all secret keys and your database URL. Then, **run the `init_database.py` script**. If it creates the tables in your database successfully, this layer is validated.

***

### ## Phase 2: Data Access Layer (Repositories)

Repositories handle all communication between your application and the database.

4.  **Repository Pattern Implementation**
    * `src/data_access/repositories/__init__.py`
    * `src/data_access/repositories/base_repository.py` (Base repository class)
    * `src/data_access/repositories/user/user_repository.py`
    * `src/data_access/repositories/channel/channel_repository.py`
    * `src/data_access/repositories/video/video_repository.py`

> **Action/Tip:** ⚙️ After reviewing these files, confirm that basic **CRUD** (Create, Read, Update, Delete) operations work. The best way to do this is to find the **unit tests** for these repositories (in the `tests/` directory) and run them.

***

### ## Phase 3: External Services Layer (API Integrations)

This layer manages communication with external APIs, primarily the YouTube Data API.

5.  **YouTube API Integration**
    * `src/external/youtube_api/__init__.py`
    * `src/external/youtube_api/exceptions.py`
    * `src/external/youtube_api/models.py` (Pydantic models for API responses)
    * `src/external/youtube_api/quota_manager.py`
    * `src/external/youtube_api/client.py` (Main API client)
    * `src/external/youtube_api/services/channel_service.py`
    * `src/external/youtube_api/services/video_service.py`
    * `src/external/youtube_api/services/analytics_service.py`

> **Action/Tip:** 📡 The goal here is to ensure you can successfully fetch data from YouTube. **Write a small, temporary script** that imports the `YouTubeAPIClient` and tries to fetch details for a single public channel or video. This confirms your API keys in `.env` are working.

***

### ## Phase 4: Business Logic Layer (Core Services)

This is the brain of your application, where data is processed and decisions are made.

6.  **Utility Classes**
    * `src/business/utils/time_utils.py`
    * `src/business/utils/data_validator.py`
    * `src/business/utils/feature_extractor.py`
7.  **Machine Learning Pipeline**
    * `src/business/ml/models/base_model.py`
    * `src/business/ml/preprocessing/feature_pipeline.py`
    * `src/business/ml/training/data_loader.py`
    * `src/business/ml/training/trainer.py`
    * `src/business/ml/evaluation/evaluator.py`
    * `src/business/ml/models/shorts_model.py`
    * `src/business/ml/models/longform_model.py`
8.  **Business Services**
    * `src/business/services/user/user_service.py`
    * `src/business/services/analytics/analytics_service.py`
    * `src/business/services/prediction/prediction_service.py` (**CORE SERVICE**)

> **Action/Tip:** 🧠 Focus on the `prediction_service.py` as it ties everything together. As you review each file in this layer, **immediately find and review its corresponding unit test**. Running tests with mock data is the fastest way to verify complex logic without needing a database or live API calls.

***

### ## Phase 5: Application Layer (API Endpoints)

This layer exposes the business logic to the outside world via a web API (Flask).

9.  **Middleware Components**
    * `src/application/middleware/cors_middleware.py`
    * `src/application/middleware/rate_limit_middleware.py`
    * `src/application/middleware/auth_middleware.py`
10. **API Routes**
    * `src/application/api/auth/routes.py`
    * `src/application/api/prediction/routes.py`
    * `src/application/api/analytics/routes.py`
    * `src/application/api/app.py` (**MAIN APPLICATION ENTRYPOINT**)

> **Action/Tip:** 🌐 Once this layer is reviewed, your backend should be fully functional. **Start the Flask server**. Use a tool like **Postman** or Insomnia to send test requests to your API endpoints (`/auth/login`, `/predict`, etc.) to ensure they work as expected.

***

### ## Phase 6: Presentation Layer (Frontend)

This is the user interface that interacts with your API.

11. **Frontend Components**
    * `src/presentation/static/css/main.css`
    * `src/presentation/static/js/main.js`
    * `src/presentation/components/chart_component.py`
    * `src/presentation/pages/auth.py`
    * `src/presentation/pages/home.py`
    * `src/presentation/pages/prediction.py`
    * `src/presentation/pages/analytics.py`
    * `src/presentation/app.py` (**MAIN FRONTEND APP**)

> **Action/Tip:** 🖥️ With the backend API running, start the frontend application. Open it in your browser and test the complete user journey. Can you log in? Can you submit a video for prediction and see a result? This is the first full end-to-end test.

***

### ## Phase 7: Data Collection & Training Scripts

These are the offline processes that gather data and train your ML models.

12. **Data Collection Pipeline**
    * `scripts/data_collection/...`
13. **Model Training Scripts**
    * `scripts/model_training/...`

> **Action/Tip:** ⏳ Review these scripts alongside the services they use (from Phases 3 and 4). Test them by running them with a **very small scope**—for example, modify a script to only collect data for one channel or train on only 100 rows of data. This ensures they work without waiting for hours.

***

### ## Phase 8: Infrastructure & Deployment

This phase prepares your application to be deployed reliably using Docker.

14. **Docker Configuration**
    * `config/docker/development/Dockerfile.dev` & `docker-compose.dev.yml`
    * `config/docker/production/Dockerfile.prod` & `docker-compose.prod.yml`
    * `config/docker/production/gunicorn.conf.py` & `nginx.conf`
15. **Deployment & Maintenance Scripts**
    * `scripts/deployment/docker/entrypoint.sh`
    * `scripts/database/backup/backup_database.py`
    * `scripts/database/maintenance/cleanup.py`

> **Action/Tip:** 🐳 To avoid issues late in the process, **try getting the development Docker setup (`docker-compose.dev.yml`) running right after you finish Phase 1**. This validates your environment setup early. Review the production files last, focusing on security and performance settings.

***

### ## Phase 9: Testing & Quality Assurance

This phase is not a final step but a continuous process integrated throughout the review.

16. **Test Infrastructure**
    * `tests/fixtures/conftest.py`
    * `tests/fixtures/mock_data.py`
17. **Unit & Integration Tests**
    * `tests/unit/...`
    * `tests/integration/...`

> **Action/Tip:** 🧪 **Do not save testing for the end**. As mentioned in the tips above, review and run the relevant tests **immediately after you review the code they cover**. This parallel approach provides constant validation and makes fixing issues much easier.