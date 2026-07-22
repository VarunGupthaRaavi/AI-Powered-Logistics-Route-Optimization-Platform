# ⚡ RouteAI Backend Engine

The backend for **RouteAI** is an asynchronous Python service built using **FastAPI**, **SQLAlchemy ORM**, **PostgreSQL**, **Alembic**, and **Google Gemini API**. It provides secure RESTful APIs for fleet management, dynamic Vehicle Routing Problem (VRP) solving, ETA prediction, and a RAG (Retrieval-Augmented Generation) AI assistant.

---

## 🏛️ Layered System Architecture

```
┌────────────────────────────────────────────────────────┐
│             FastAPI Routers (app/api/)                 │
└──────────────────────────┬─────────────────────────────┘
                           │ Request Validation (Schemas)
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
│ PostgreSQL 15 Database      │
└─────────────────────────────┘
```

---

## 📁 Application Structure (`app/`)

```
app/
├── api/             # API Endpoints organized by domain
│   ├── auth/        # User authentication & token issuance
│   ├── users/       # User management
│   ├── customers/   # Customer records
│   ├── drivers/     # Driver roster & status updates
│   ├── vehicles/    # Vehicle fleet telemetry
│   ├── deliveries/  # Delivery package orders & time windows
│   ├── routes/      # Route dispatching & waypoint sequence
│   ├── scheduling/  # Shift schedules & depot dispatch windows
│   ├── analytics/   # Logistics performance metrics
│   ├── ai/          # Route optimization triggers & Gemini prompts
│   ├── rag/         # Vector document querying over fleet policies
│   └── notifications/# Dispatch alerts & vehicle breakdown notifications
│
├── models/          # SQLAlchemy Database Models (User, Driver, Vehicle, Delivery, Route)
├── schemas/         # Pydantic v2 validation models for request/response serialization
├── services/        # Core business logic layer (AuthService, RouteService, AIService)
├── repositories/    # Data Access Layer implementing Repository Pattern
├── database/        # Engine creation, SessionLocal generator, and Base model
├── middleware/      # Request logging, rate limiting & auth middleware
├── security/        # JWT creation/verification & Bcrypt password hashing
├── ai/              # AI Optimization Engines
│   ├── route_optimizer/  # VRP constraint solver & Gemini route optimizer
│   ├── eta_prediction/   # Machine-learning ETA & delay risk estimation
│   ├── dynamic_routing/  # Real-time incident response rerouting
│   ├── multi_agent/      # Autonomous driver dispatch agent coordinator
│   ├── rag/              # Fleet knowledgebase retrieval engine
│   └── prompts/          # Versioned Gemini system prompts
├── utils/           # Distance calculation (Haversine/Geospatial) & date helpers
├── config/          # Environment configuration using pydantic-settings
├── core/            # Custom exception classes (EntityNotFound, AuthFailed)
└── main.py          # FastAPI application initialization & middleware setup
```

---

## 🛠️ Local Development & Migration Setup

### 1. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS:
source venv/bin/activate

# Activate on Windows:
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Update `DATABASE_URL` and set your `GEMINI_API_KEY`.

### 3. Database Migrations (Alembic)

Initialize and run database schema migrations against PostgreSQL:

```bash
# Generate a new migration revision (when models change)
alembic revision --autogenerate -m "Add vehicle capacity columns"

# Upgrade database to latest revision
alembic upgrade head

# Rollback one migration revision
alembic downgrade -1
```

### 4. Run Development Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Server runs at `http://127.0.0.1:8000`.

---

## 🧪 Running Automated Tests

Pytest test suites are located under `tests/`:

```bash
# Run all tests
pytest -v

# Run API test suite only
pytest tests/api/ -v

# Run AI module test suite
pytest tests/ai/ -v
```

---

## 🔒 Security & JWT Flow

1. User sends credentials to POST `/api/v1/auth/login`.
2. Backend verifies password hash using Bcrypt (`passlib`).
3. Upon success, backend issues a signed JWT Bearer Token containing user ID and role claims.
4. Protected API endpoints enforce token validation via FastAPI dependency injection.
