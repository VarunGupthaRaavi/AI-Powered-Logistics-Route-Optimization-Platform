# 🚚 RouteAI — Enterprise AI-Powered Logistics & Route Optimization Platform

> **Next-generation logistics dispatch, real-time vehicle routing problem (VRP) solving, predictive ETAs, multi-agent fleet dispatching, and conversational intelligence powered by Google Gemini API.**

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [AI Subsystems](#-ai-subsystems)
- [Getting Started & Local Development](#-getting-started--local-development)
  - [Prerequisites](#prerequisites)
  - [Option 1: Quickstart with Docker Compose (Recommended)](#option-1-quickstart-with-docker-compose-recommended)
  - [Option 2: Manual Step-by-Step Local Setup](#option-2-manual-step-by-step-local-setup)
- [Environment Configuration](#-environment-configuration)
- [API Documentation & Testing](#-api-documentation--testing)
- [Directory Structure](#-directory-structure)
- [Production Deployment](#-production-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📦 Overview

Modern enterprise logistics operations face constant unpredictable challenges: severe traffic delays, sudden weather anomalies, emergency order injections, vehicle breakdowns, and strict delivery time windows. Standard static routing systems fail under such dynamic conditions.

**RouteAI** is a state-of-the-art enterprise logistics management platform built to transform fleet operations. By combining mathematical solver algorithms with **Google Gemini 2.5 AI models**, RouteAI delivers autonomous route optimization, real-time incident rerouting, machine-learning powered ETA predictions, and natural language dispatch intelligence.

---

## ✨ Key Features

- 🗺️ **Dynamic Vehicle Routing Solver (VRP)**: Solves complex multi-depot, multi-vehicle routing problems while strictly respecting vehicle capacity constraints, time windows, and driver break schedules.
- ⚡ **Real-Time Mid-Route Incident Adjustment**: Automatically detects traffic congestion or breakdown events and re-optimizes active driver routes on the fly.
- ⏱️ **ML-Driven Predictive ETAs**: Generates accurate arrival estimations by analyzing historical delivery metrics, road speed profiles, and ambient weather telemetry.
- 🤖 **Multi-Agent Fleet Coordination**: Autonomous agent negotiation model that automatically balances order loads across nearby active drivers based on proximity and capacity.
- 💬 **Logistics RAG Assistant (Gemini API)**: Conversational assistant for dispatchers and fleet managers to query operating policies, driver compliance records, and active delivery statuses in natural language.
- 📊 **Interactive Operations Dashboard**: High-visibility mission control dashboard built with React and Tailwind CSS for real-time fleet tracking, order assignment, and logistics KPIs.

---

## 🏗️ Architecture & Tech Stack

```
                               ┌───────────────────────────┐
                               │     React + Vite Client   │
                               │  (Tailwind CSS Dashboard) │
                               └─────────────┬─────────────┘
                                             │ HTTP / REST API
                                             ▼
                               ┌───────────────────────────┐
                               │   FastAPI Backend Engine  │
                               │  (Async Python Service)   │
                               └──────┬─────────────────┬──┘
                                      │                 │
                      SQLAlchemy ORM │                 │ Google Gemini API / SDK
                                      ▼                 ▼
                       ┌────────────────────┐    ┌────────────────────┐
                       │  PostgreSQL 15 DB  │    │  Google Gemini AI  │
                       │  (Vector + Rel)    │    │ (VRP & RAG Engine) │
                       └────────────────────┘    └────────────────────┘
```

### Stack Components

| Layer | Technology | Key Libraries / Frameworks |
|---|---|---|
| **Frontend** | React 18 (Vite) | Tailwind CSS, Lucide Icons, Axios, React Router 6 |
| **Backend** | Python 3.11+ | FastAPI, Uvicorn, Pydantic v2, AsyncIO |
| **Database** | PostgreSQL 15 | SQLAlchemy 2.0 (Async ORM), Alembic Migrations |
| **Authentication** | JWT & Security | PyJWT, Passlib (Bcrypt hashing), Bearer Token Auth |
| **AI & LLM** | Google Gemini API | `google-genai` SDK, Vector Embeddings (RAG) |
| **Containers** | Docker | Docker Compose, Multi-stage Dockerfiles |
| **Deployment** | Cloud Platforms | Vercel (Frontend), Railway (Backend & Postgres) |

---

## 🧠 AI Subsystems

The backend AI module (`app/ai/`) consists of 6 dedicated engines:

1. **`route_optimizer`**: Multi-objective routing solver combining Google Gemini reasoning with constraint satisfaction algorithms.
2. **`eta_prediction`**: Predictive engine for estimated travel times and delay risk probabilities.
3. **`dynamic_routing`**: Real-time event listener that calculates low-overhead route modifications during active delivery runs.
4. **`multi_agent`**: Dispatch agent orchestrator that resolves load-balancing tasks across autonomous driver agents.
5. **`rag`**: Retrieval-Augmented Generation pipeline over vectorized enterprise manuals, schedules, and compliance docs.
6. **`prompts`**: Curated, versioned prompt templates for structured Gemini AI responses.

---

## 🚀 Getting Started & Local Development

### Prerequisites

Ensure you have the following installed on your machine:
- **Node.js**: `v18.0.0` or higher
- **npm**: `v9.0.0` or higher
- **Python**: `v3.11.0` or higher
- **PostgreSQL**: `v15.0` or higher (optional if using Docker)
- **Docker & Docker Compose**: (Recommended for easiest setup)
- **Google Gemini API Key**: Obtainable from [Google AI Studio](https://aistudio.google.com/)

---

### Option 1: Quickstart with Docker Compose (Recommended)

Run the entire application stack (PostgreSQL database, FastAPI backend, and React frontend) in isolated containers with a single command:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/route-ai.git
cd route-ai

# 2. Set up environment key (Optional: insert your GEMINI_API_KEY)
export GEMINI_API_KEY="your_actual_gemini_api_key_here"

# 3. Launch all services
docker-compose up --build
```

#### Accessing Services:
- 🌐 **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- ⚡ **Backend API Root**: [http://localhost:8000](http://localhost:8000)
- 📖 **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 🐘 **PostgreSQL Database**: `localhost:5432` (`user: routeai`, `password: routeai_secret`, `db: routeai_db`)

To stop the environment:
```bash
docker-compose down -v
```

---

### Option 2: Manual Step-by-Step Local Setup

If you prefer running the services directly on your local system:

#### Step 1: Start PostgreSQL Database
Ensure a local PostgreSQL instance is running on port `5432`. Create a database named `routeai_db`:
```sql
CREATE DATABASE routeai_db;
CREATE USER routeai WITH PASSWORD 'routeai_secret';
GRANT ALL PRIVILEGES ON DATABASE routeai_db TO routeai;
```

#### Step 2: Set Up Backend (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment configuration file
cp .env.example .env

# Edit .env file and add your GEMINI_API_KEY if available
```

Run database migrations via Alembic:
```bash
# Apply migrations to local database
alembic upgrade head
```

Launch the FastAPI development server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*Backend server will start at `http://127.0.0.1:8000`.*

#### Step 3: Set Up Frontend (React + Vite)

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node modules
npm install

# Create frontend environment configuration
cp .env.example .env

# Launch Vite development server
npm run dev
```
*Frontend application will start at `http://localhost:3000`.*

---

## ⚙️ Environment Configuration

### Backend Environment Variables (`backend/.env`)

```ini
# Application Configuration
PROJECT_NAME="RouteAI"
API_V1_STR="/api/v1"

# Security & JWT Token
SECRET_KEY="super_secret_jwt_key_change_in_production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database Connections
DATABASE_URL="postgresql://routeai:routeai_secret@localhost:5432/routeai_db"
ASYNC_DATABASE_URL="postgresql+asyncpg://routeai:routeai_secret@localhost:5432/routeai_db"

# AI Integration
GEMINI_API_KEY="your_google_gemini_api_key"
GEMINI_MODEL="gemini-2.5-flash"

# CORS Allowed Origins
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

### Frontend Environment Variables (`frontend/.env`)

```ini
VITE_API_BASE_URL="http://localhost:8000/api/v1"
VITE_APP_NAME="RouteAI"
VITE_GOOGLE_MAPS_API_KEY="your_google_maps_key"
```

---

## 📑 API Documentation & Testing

### Interactive API Explorer
FastAPI automatically generates interactive OpenAPI documentation:
- **Swagger UI**: Visit [http://localhost:8000/docs](http://localhost:8000/docs) to test API endpoints directly from your browser.
- **ReDoc Format**: Visit [http://localhost:8000/redoc](http://localhost:8000/redoc) for clean, readable technical documentation.

### Running Backend Unit & Integration Tests
```bash
cd backend
pytest -v
```

---

## 📂 Directory Structure

```
route-ai/
├── frontend/                 # React + Vite + Tailwind CSS Client
│   ├── public/               # Static assets & favicon
│   ├── src/                  # Source code
│   │   ├── assets/           # Media & icons
│   │   ├── components/       # UI & Domain components (dashboard, delivery, driver, etc.)
│   │   ├── layouts/          # Main & Auth layout wrappers
│   │   ├── pages/            # Application view pages
│   │   ├── hooks/            # Custom React hooks
│   │   ├── context/          # Global Auth & App context state
│   │   ├── services/         # Client-side API integration services
│   │   ├── api/              # Axios HTTP client configuration
│   │   ├── utils/            # Helper functions & formatters
│   │   ├── constants/        # Application constants & enums
│   │   ├── routes/           # React Router route definitions
│   │   ├── styles/           # Global Tailwind CSS styles
│   │   ├── App.jsx           # App root component
│   │   └── main.jsx          # React entry point
│   ├── package.json          # Node dependencies & build scripts
│   ├── vite.config.js        # Vite bundler configuration
│   └── tailwind.config.js    # Custom Tailwind styling theme
│
├── backend/                  # FastAPI Python Service
│   ├── app/                  # Application core
│   │   ├── api/              # API Endpoints (auth, drivers, routes, ai, rag, etc.)
│   │   ├── models/           # SQLAlchemy ORM Database Models
│   │   ├── schemas/          # Pydantic Request/Response Validation Schemas
│   │   ├── services/         # Core business logic layer
│   │   ├── repositories/     # Data access abstraction pattern
│   │   ├── database/         # Database engine & SessionLocal factory
│   │   ├── middleware/       # Custom logging & auth middleware
│   │   ├── security/         # JWT generation, validation & password hashing
│   │   ├── ai/               # AI Engine (optimizer, eta, multi-agent, rag, prompts)
│   │   ├── utils/            # Helper utilities & geospatial math
│   │   ├── config/           # Application settings using Pydantic
│   │   ├── core/             # Custom exception handlers
│   │   └── main.py           # FastAPI application entry point
│   ├── tests/                # Pytest test suites (api, services, ai, integration)
│   ├── alembic/              # Database schema migration scripts
│   ├── requirements.txt      # Python dependencies
│   └── alembic.ini           # Alembic configuration
│
├── docs/                     # Engineering & Operations Documentation
│   ├── architecture/         # System architecture breakdowns
│   ├── api/                  # API specification standards
│   ├── database/             # ER diagrams & schema documentation
│   ├── diagrams/             # Sequence & workflow diagrams
│   ├── ai/                   # AI & Gemini integration details
│   ├── deployment/           # Production deployment playbooks
│   └── user-guide/           # Operations user manual
│
├── scripts/                  # Management & Automation Scripts
│   ├── setup.sh              # Unix/macOS environment initializer
│   ├── setup.ps1             # Windows PowerShell environment initializer
│   ├── seed_database.py      # Database seeding script
│   └── reset_database.py     # Database reset script
│
├── .github/workflows/        # CI/CD Workflows for GitHub Actions
├── docker/                   # Dockerfiles for frontend, backend & postgres
├── docker-compose.yml        # Development multi-container orchestration
├── LICENSE                   # Open Source MIT License
├── CONTRIBUTING.md           # Guidelines for repository contributors
└── README.md                 # Root Repository README
```

---

## 🌐 Production Deployment

### Frontend (Vercel)
The React client is pre-configured for seamless deployment on **Vercel**:
1. Connect your GitHub repository to Vercel.
2. Set Root Directory to `frontend`.
3. Set Build Command to `npm run build` and Output Directory to `dist`.
4. Configure Environment Variable: `VITE_API_BASE_URL=https://your-backend-railway-url.com/api/v1`.

### Backend & Database (Railway)
The FastAPI service and PostgreSQL database are optimized for deployment on **Railway**:
1. Provision a PostgreSQL Database on Railway.
2. Deploy the `backend` service targeting Python 3.11.
3. Configure environment variables (`DATABASE_URL`, `JWT_SECRET_KEY`, `GEMINI_API_KEY`).
4. Set start command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

---

## 🤝 Contributing

We welcome contributions from developers, data scientists, and logistics domain experts! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) guide for instructions on submitting pull requests, coding standards, and branch policies.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for complete details.
