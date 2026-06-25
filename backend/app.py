from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from database import execute_query, execute_custom_query
from ai_utils import ask_ai
from report_generator import generate_report, generate_custom_report
from pdf_generator import create_pdf
from datetime import datetime, timedelta
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import os
import glob
import logging
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

logger = logging.getLogger(__name__)

def cleanup_old_pdfs(days=7):
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        return
    cutoff = datetime.now() - timedelta(days=days)
    for filepath in glob.glob(os.path.join(reports_dir, "*.pdf")):
        if datetime.fromtimestamp(os.path.getmtime(filepath)) < cutoff:
            os.remove(filepath)
            logger.info(f"Deleted old PDF: {filepath}")

cleanup_old_pdfs()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("CORS_ORIGIN", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

REPORT_ALIASES = {
    "complaint": "complaint",
    "complaints": "complaint",
    "complaint report": "complaint",
    "revenue": "revenue",
    "revenue report": "revenue",
    "branch": "branch",
    "branch report": "branch",
    "customer satisfaction": "customer_satisfaction",
    "customer satisfaction report": "customer_satisfaction"
}

class AskRequest(BaseModel):
    question: str

class ReportRequest(BaseModel):
    report_type: str

class CustomReportRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Customer Analysis Backend Running"}


@app.get("/health")
def health():
    return {"success": True, "status": "healthy", "error": None}


@app.post("/ask")
@limiter.limit("10/minute")
def ask_question(request: Request, body: AskRequest):
    return ask_ai(body.question)


@app.post("/report")
@limiter.limit("5/minute")
def create_report(request: Request, body: ReportRequest):
    start_time = time.time()
    report_type = REPORT_ALIASES.get(
        body.report_type.lower().strip(),
        body.report_type.lower().strip()
    )

    report = generate_report(report_type)

    if report is None:
        return {
            "success": False,
            "report": None,
            "error": "Invalid report type"
        }

    return {
        "success": True,
        "report_type": body.report_type,
        "report": report,
        "generation_time": round(time.time() - start_time, 2),
        "error": None
    }


@app.post("/report/custom")
@limiter.limit("5/minute")
def custom_report(request: Request, body: CustomReportRequest):
    start_time = time.time()

    report = generate_custom_report(body.question)

    return {
        "success": True,
        "question": body.question,
        "report": report,
        "generation_time": round(time.time() - start_time, 2),
        "error": None
    }


@app.post("/report/pdf")
@limiter.limit("5/minute")
def create_report_pdf(request: Request, body: ReportRequest):
    start_time = time.time()
    report_type = REPORT_ALIASES.get(
        body.report_type.lower().strip(),
        body.report_type.lower().strip()
    )

    report = generate_report(report_type)

    if report is None:
        return {
            "success": False,
            "file": None,
            "error": "Invalid report type"
        }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{body.report_type.lower()}_report_{timestamp}.pdf"

    create_pdf(report, filename)

    return {
        "success": True,
        "report_type": body.report_type,
        "file": filename,
        "download_url": f"/download-report/{filename}",
        "generation_time": round(time.time() - start_time, 2),
        "error": None
    }


@app.get("/download-report/{filename}")
def download_report(filename: str):
    file_path = f"reports/{filename}"
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )


@app.get("/dashboard")
@limiter.limit("30/minute")
def dashboard(request: Request):
    summary = {
        "customers": execute_query("SELECT COUNT(*) FROM customers;")[0][0],
        "calls": execute_query("SELECT COUNT(*) FROM calls;")[0][0],
        "services": execute_query("SELECT COUNT(*) FROM services;")[0][0],
        "surveys": execute_query("SELECT COUNT(*) FROM surveys;")[0][0]
    }

    complaints = execute_query("""
        SELECT issue_category, COUNT(*) AS complaints
        FROM calls
        WHERE call_type = 'Complaint'
        GROUP BY issue_category
        ORDER BY complaints DESC
        LIMIT 5;
    """)

    revenue = execute_query("""
        SELECT service_type, SUM(service_cost) AS revenue
        FROM services
        GROUP BY service_type
        ORDER BY revenue DESC
        LIMIT 5;
    """)

    ratings = execute_query("""
        SELECT c.branch, ROUND(AVG(s.customer_rating), 2)
        FROM surveys s
        JOIN services sv ON s.service_id = sv.service_id
        JOIN calls c ON sv.call_id = c.call_id
        GROUP BY c.branch
        ORDER BY 2 DESC
        LIMIT 10;
    """)

    return {
        "success": True,
        "summary": summary,
        "complaints": [{"name": row[0], "value": row[1]} for row in complaints],
        "revenue": [{"service": row[0], "revenue": row[1]} for row in revenue],
        "ratings": [{"branch": row[0], "rating": row[1]} for row in ratings],
        "error": None
    }
