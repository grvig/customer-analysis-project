# Customer Analysis Project

Internal business intelligence tool for analysing customer data, complaints, revenue, and branch performance. Built with FastAPI (backend) and React/Electron (frontend), using a local Ollama AI model for natural language queries and report generation.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React, Vite, Electron |
| Database | PostgreSQL |
| AI | Ollama (qwen2.5-coder:7b) |

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL
- [Ollama](https://ollama.com) with `qwen2.5-coder:7b` pulled (`ollama pull qwen2.5-coder:7b`)

### 1. Environment variables

Copy `.env.example` to `.env` in the project root and fill in your values:

```
DB_HOST=localhost
DB_NAME=customer_analysis
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

CORS_ORIGIN=http://localhost:5173

AI_TIMEOUT=60

JWT_SECRET=your_jwt_secret_here
```

`JWT_SECRET` can be any long random string. Generate one with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> **Mac users:** use `python3` instead of `python`. If you get a Postgres authentication error, set `DB_HOST=127.0.0.1` instead of `localhost` — Mac resolves `localhost` over IPv6 which can cause connection failures.

Copy `tempapp/.env.example` to `tempapp/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
uvicorn app:app --reload
```

Backend runs at `http://localhost:8000`.

### 3. Frontend

```bash
cd tempapp
npm install
npm run dev        # browser at http://localhost:5173
npm run electron   # desktop app
```

---

## Running tests

```bash
cd backend
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pytest tests/ -v
```

---

## API Endpoints

| Method | Endpoint | Description | Auth required | Rate limit |
|---|---|---|---|---|
| GET | `/` | Health check | No | — |
| GET | `/health` | Health check with status | No | — |
| POST | `/login` | Login and receive JWT token | No | — |
| POST | `/register` | Create a new user account | No | — |
| POST | `/change-password` | Change authenticated user's password | Yes | — |
| GET | `/dashboard` | Dashboard summary data | Yes | 30/min |
| POST | `/ask` | Natural language AI query | Yes | 10/min |
| POST | `/report` | Generate preset report | Yes | 5/min |
| POST | `/report/custom` | Generate custom AI report | Yes | 5/min |
| POST | `/report/pdf` | Generate PDF report | Yes | 5/min |
| GET | `/download-report/{filename}` | Download generated PDF | Yes | — |

### Preset report types

`complaint`, `revenue`, `branch`, `customer_satisfaction`

---

## Project Structure

```
customer-analysis-project/
├── dataset/                     # Raw CSV source data
├── backend/
│   ├── app.py                   # FastAPI routes and middleware
│   ├── auth.py                  # Login, register, JWT issuance, change password
│   ├── init_auth.py             # Creates users table on startup
│   ├── database.py              # DB connection and query execution
│   ├── ai_utils.py              # AI query generation, validation, and execution
│   ├── report_generator.py      # Preset and custom report generation
│   ├── pdf_generator.py         # PDF creation
│   ├── config.py                # AI model config
│   ├── schema_context.txt       # Database schema provided to AI
│   ├── ai_test_cases.txt        # Manual AI query test cases
│   ├── app.log                  # Application log (auto-generated)
│   └── tests/
│       ├── test_app.py          # API endpoint tests
│       ├── test_utils.py        # Utility function tests
│       └── test_pdf.py          # PDF generation tests
└── tempapp/
    └── src/
        ├── pages/               # Dashboard, AIAssistant, Reports, Login, CreateUser
        ├── components/          # Layout, Sidebar, Header, ProtectedRoute, charts
        ├── services/            # api.js, authService, dashboardService, aiService, reportService
        └── index.css            # Global styles and CSS variables
```
