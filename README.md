
# Workspace API

A production-style REST API for managing users and projects, built with **FastAPI**, **PostgreSQL**, **JWT authentication**, and **Redis**.

The project is containerized with Docker, tested using GitHub Actions, and deployed automatically to Render after successful CI checks.

## 🚀 Live Demo

- **API:** https://workspace-api-jnr2.onrender.com
- **Swagger Documentation:** https://workspace-api-jnr2.onrender.com/docs
- **OpenAPI Schema:** https://workspace-api-jnr2.onrender.com/openapi.json

## ✨ Features

- User registration and login
- JWT-based authentication
- Protected user profile endpoint
- User CRUD operations
- Project CRUD operations
- User-project ownership relationship
- PostgreSQL database integration
- Alembic database migrations
- Redis integration for caching/rate limiting
- Docker and Docker Compose support
- Automated testing with Pytest
- Continuous Integration using GitHub Actions
- Continuous Deployment through Render

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT |
| Password Hashing | Passlib |
| Caching / Rate Limiting | Redis |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |
| CI | GitHub Actions |
| Deployment | Render |

## 📁 Project Structure

```text
workspace-api/
│
├── app/
│   ├── api/
│   │   ├── users.py
│   │   ├── projects.py
│   │   └── auth.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── redis.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   └── main.py
│
├── alembic/
├── tests/
│   └── test_basic.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .dockerignore
└── README.md
```

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/shreyagupta1181/workspace-api.git
cd workspace-api
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Never commit `.env` or expose real credentials publicly.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 🐳 Running with Docker Compose

Start the application and PostgreSQL:

```bash
docker compose up -d --build
```

Run migrations inside the API container:

```bash
docker compose exec api alembic upgrade head
```

View running containers:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs -f api
```

Stop the containers:

```bash
docker compose down
```

> PostgreSQL data is stored in a Docker volume so it persists across container restarts.

## 🧪 Running Tests

Run the test suite locally:

```bash
python -m pytest
```

The GitHub Actions workflow automatically runs the tests when:

- A commit is pushed to `main`
- A pull request targets `main`

## 🔄 CI/CD Pipeline

```text
Developer pushes code
        ↓
GitHub Actions starts
        ↓
Dependencies are installed
        ↓
Automated tests run
        ↓
Tests pass ✅
        ↓
Render deploys automatically
        ↓
Live API is updated 🚀
```

If the tests fail, Render does not deploy that commit because deployment is configured to occur only after CI checks pass.

## 📚 API Documentation

FastAPI automatically generates interactive documentation.

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

You can use Swagger UI to inspect and test the available endpoints.

## 🔐 Security Notes

- Secrets are stored in environment variables.
- The `.env` file is excluded from Git.
- Passwords are hashed before storage.
- Protected routes require valid JWT authentication.
- Production credentials should never be committed to the repository.

## 🔮 Future Improvements

- Add more comprehensive unit and integration tests
- Add database service containers to CI
- Add role-based access control
- Add refresh-token support
- Add API versioning
- Add monitoring and structured logging
- Improve automated documentation and deployment checks

## 👩‍💻 Author

**Shreya Gupta**

GitHub: [@shreyagupta1181](https://github.com/shreyagupta1181)