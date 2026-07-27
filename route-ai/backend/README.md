# ⚡ RouteAI Backend Engine

The backend for **RouteAI** is an enterprise-grade asynchronous Python service built using **FastAPI**, **SQLAlchemy 2.0 ORM**, **PostgreSQL**, **Alembic**, **Pydantic v2 Settings**, **Passlib (bcrypt)**, **python-jose**, and the **Google Gemini API**. It provides secure RESTful APIs for fleet management, dynamic Vehicle Routing Problem (VRP) solving, ETA prediction, Role-Based Access Control (RBAC), and a RAG (Retrieval-Augmented Generation) AI assistant.

---

## 🏛️ Layered System Architecture

```
┌────────────────────────────────────────────────────────┐
│             FastAPI Routers (app/api/)                 │
└──────────────────────────┬─────────────────────────────┘
                           │ Request Validation (Pydantic Schemas)
                           ▼
┌────────────────────────────────────────────────────────┐
│             Service Layer (app/services/)              │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
               ▼                          ▼
┌─────────────────────────────┐ ┌────────────────────────┐
│ Repository / Database Layer │ │  AI Subsystem Layer    │
│  (app/repositories/ &       │ │      (app/ai/)         │
│   app/database/)            │ │ (Gemini API & VRP)     │
└──────────────┬──────────────┘ └────────────────────────┘
               │
               ▼
┌─────────────────────────────┐
│ PostgreSQL Database         │
└─────────────────────────────┘
```

---

## 📁 Project Structure

```
backend/
├── alembic/                 # Alembic environment and database migration scripts
│   ├── versions/            # Database schema revision scripts
│   ├── env.py               # Migration environment config with Base.metadata autogeneration
│   └── script.py.mako       # Migration template script
├── app/
│   ├── api/                 # API Routers & Endpoints
│   │   ├── auth/            # Auth endpoints (POST /register, POST /login, GET /me)
│   │   ├── users/           # User management endpoints
│   │   ├── customers/       # Customer directory
│   │   ├── drivers/         # Driver roster & status
│   │   ├── vehicles/        # Vehicle fleet telemetry
│   │   ├── deliveries/      # Package orders & time windows
│   │   ├── routes/          # Dispatching & waypoint sequence
│   │   ├── scheduling/      # Shifts & depot dispatch windows
│   │   ├── analytics/       # Logistics performance metrics
│   │   ├── ai/              # Optimization triggers & Gemini prompts
│   │   ├── rag/             # Vector document search over fleet policies
│   │   ├── notifications/   # Dispatch & alert notifications
│   │   └── router.py        # Centralized APIRouter aggregation
│   ├── config/              # Pydantic Settings configuration (settings.py)
│   ├── database/            # Database session engine, SessionLocal, and Base
│   ├── models/              # SQLAlchemy 2.0 ORM models (User, Role, Driver, Route, etc.)
│   ├── repositories/        # Data Access Layer implementing Repository Pattern (UserRepository)
│   ├── schemas/             # Pydantic v2 request/response validation schemas (auth.py, user.py)
│   ├── security/            # Security module (password hashing, JWT handling, RBAC dependencies)
│   │   ├── password.py      # Bcrypt password hashing & verification using Passlib
│   │   ├── jwt.py           # JWT token generation, verification, and decoding using python-jose
│   │   └── dependencies.py  # get_current_user & require_role RBAC dependencies
│   ├── services/            # Core business logic layer (AuthService)
│   ├── ai/                  # AI Route Optimization & RAG modules
│   └── main.py              # FastAPI application initialization & OpenAPI Swagger configuration
├── tests/                   # Automated test suite using Pytest and TestClient
│   ├── api/                 # API and Authentication tests (test_auth.py)
│   └── conftest.py          # In-memory test database and fixture overrides
├── .env.example             # Example environment variable template
├── alembic.ini              # Alembic configuration file
├── requirements.txt         # Python package dependencies
└── README.md                # Backend documentation
```

---

## 🛠️ Backend Setup & Configuration

### 1. Setup Virtual Environment

```bash
# Navigate to backend directory
cd route-ai/backend

# Create virtual environment
python -m venv .venv

# Activate on Linux/macOS:
source .venv/bin/activate

# Activate on Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt
```

### 2. Configure PostgreSQL Database

Ensure PostgreSQL is running locally or accessible via network. Create a database instance:

```sql
CREATE DATABASE routeai_db;
CREATE USER routeai_user WITH PASSWORD 'routeai_password';
GRANT ALL PRIVILEGES ON DATABASE routeai_db TO routeai_user;
```

### 3. Environment Variables Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Configure your `.env` settings:

```env
PROJECT_NAME="RouteAI"
API_V1_STR="/api/v1"
DATABASE_URL="postgresql://routeai_user:routeai_password@localhost:5432/routeai_db"
SECRET_KEY="your-super-secret-jwt-signing-key-min-32-chars-long"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
GEMINI_API_KEY="your-gemini-api-key"
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

---

## 🗄️ Database Migrations (Alembic)

Alembic is configured to automatically inspect SQLAlchemy models registered in `app/models/__init__.py` against the PostgreSQL schema using `Base.metadata`.

### Execution Commands:

```bash
# 1. Apply existing database migrations to update PostgreSQL schema to latest head
alembic upgrade head

# 2. Autogenerate a new migration after adding/modifying SQLAlchemy models
alembic revision --autogenerate -m "Add new model feature"

# 3. Rollback the database by 1 revision step
alembic downgrade -1

# 4. Check current migration version status
alembic current
```

---

## 🚀 Running the FastAPI Development Server

Start the application with Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The application server will start at: `http://127.0.0.1:8000`

---

## 📖 Swagger OpenAPI Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema JSON**: [http://127.0.0.1:8000/api/v1/openapi.json](http://127.0.0.1:8000/api/v1/openapi.json)

### Using JWT Authentication in Swagger UI:
1. Click the **Authorize 🔓** button at the top right of the Swagger UI.
2. Enter your registered account credentials (`username` = email, `password`).
3. Click **Authorize** to inject the `Bearer <token>` into subsequent API test calls.

---

## 🔒 Authentication & Security Architecture

### 1. Password Hashing (`app/security/password.py`)
- Passlib with `bcrypt` scheme.
- Plain text passwords are **never** persisted in the database.
- `hash_password(password: str)` and `verify_password(plain, hashed)` utilities.

### 2. JWT Token Issuance & Decoding (`app/security/jwt.py`)
- Powered by `python-jose`.
- `create_access_token(data: dict, expires_delta)` signs tokens using `SECRET_KEY` and `ALGORITHM` (HS256).
- Token payload contains user ID (`sub`), `email`, and assigned `role`.

### 3. Authentication Dependency (`app/security/dependencies.py`)
- `get_current_user`: FastAPI dependency extracting `OAuth2PasswordBearer` token, decoding payload claims, and fetching active `User` record from PostgreSQL via `UserRepository`.

### 4. Role-Based Access Control (RBAC) (`app/security/dependencies.py`)
- `require_role(*allowed_roles: str)`: Enforces role permissions on protected endpoints.
- Usage: `Depends(require_role("Admin"))` or `Depends(require_role("Admin", "User"))`.
- Returns `HTTP 403 Forbidden` if user does not possess the required role.

### 5. Authentication APIs (`app/api/auth/router.py`)

| Method | Endpoint | Access | Summary | Description |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Public | Register Account | Validates request, checks email uniqueness, hashes password, assigns default "User" role, stores user (Returns `201 Created`). |
| `POST` | `/api/v1/auth/login` | Public | User Login | Authenticates credentials, verifies bcrypt hash, generates and returns JWT Bearer token (Returns `200 OK`). |
| `GET` | `/api/v1/auth/me` | Protected | Authenticated Profile | Returns the profile of the current user parsed from Bearer token (Returns `200 OK`). |

---

## 🧪 Running Automated Tests

Run the Pytest suite covering security, JWT, registration, login, role access, repositories, and services:

```bash
# Run all automated tests
pytest route-ai/backend/tests/ -v

# Run authentication API tests only
pytest route-ai/backend/tests/api/test_auth.py -v
```
