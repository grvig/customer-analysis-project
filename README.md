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
```

Copy `tempapp/.env.example` to `tempapp/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
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
venv\Scripts\activate
pytest tests/ -v
```

---

## API Endpoints

| Method | Endpoint | Description | Rate limit |
|---|---|---|---|
| GET | `/` | Health check | — |
| GET | `/health` | Health check with status | — |
| GET | `/dashboard` | Dashboard summary data | 30/min |
| POST | `/ask` | Natural language AI query | 10/min |
| POST | `/report` | Generate preset report | 5/min |
| POST | `/report/custom` | Generate custom AI report | 5/min |
| POST | `/report/pdf` | Generate PDF report | 5/min |
| GET | `/download-report/{filename}` | Download generated PDF | — |

### Preset report types

`complaint`, `revenue`, `branch`, `customer_satisfaction`

---

## Project Structure

```
customer-analysis-project/
├── backend/
│   ├── app.py               # FastAPI routes
│   ├── database.py          # DB connection and query execution
│   ├── ai_utils.py          # AI query generation and execution
│   ├── report_generator.py  # Preset and custom report generation
│   ├── pdf_generator.py     # PDF creation
│   ├── config.py            # Model config
│   ├── schema_context.txt   # Database schema provided to AI
│   ├── sql_history.txt      # AI query audit log (auto-generated)
│   ├── app.log              # Application log (auto-generated)
│   └── tests/
│       ├── test_app.py      # API endpoint tests
│       └── test_utils.py    # Utility function tests
└── tempapp/
    └── src/
        ├── pages/           # Dashboard, AIAssistant, Reports
        ├── components/      # Layout, charts
        └── services/        # API service functions
```
