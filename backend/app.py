from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from database import execute_query, execute_custom_query
from ai_utils import ask_ai
from report_generator import generate_report
from pdf_generator import create_pdf
from datetime import datetime, timedelta
import time
import os
import glob
import logging
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

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


from report_generator import (
    generate_report,
    generate_custom_report
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("CORS_ORIGIN", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    sql: str

    @field_validator("sql")
    @classmethod
    def must_be_select(cls, v):
        if not v.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")
        return v

class AskRequest(BaseModel):
    question: str

class ReportRequest(BaseModel):
    report_type: str
    
class CustomReportRequest(BaseModel):
    question: str

@app.get("/")
def home():

    return {
        "message": "Customer Analysis Backend Running"
    }

@app.get("/customers/count")
def customer_count():

    rows = execute_query(
        "SELECT COUNT(*) FROM customers;"
    )

    return {
        "customer_count": rows[0][0]
    }

@app.get("/calls/count")
def call_count():

    rows = execute_query(
        "SELECT COUNT(*) FROM calls;"
    )

    return {
        "call_count": rows[0][0]
    }

@app.get("/services/count")
def service_count():

    rows = execute_query(
        "SELECT COUNT(*) FROM services;"
    )

    return {
        "service_count": rows[0][0]
    }

@app.get("/surveys/count")
def survey_count():

    rows = execute_query(
        "SELECT COUNT(*) FROM surveys;"
    )

    return {
        "survey_count": rows[0][0]
    }

@app.post("/query")
def run_query(request: QueryRequest):

    rows = execute_custom_query(
        request.sql
    )

    return {
        "rows": rows
    }

@app.post("/ask")
def ask_question(request: AskRequest):

    return ask_ai(
        request.question
    )

@app.post("/report")
def create_report(request: ReportRequest):
    start_time = time.time()
    report_type = (
        request.report_type
        .lower()
        .strip()
    )

    aliases = {
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

    report_type = aliases.get(
        report_type,
        report_type
    )

    report = generate_report(
        report_type
    )

    if report is None:
        return {
            "success": False,
            "report": None,
            "error": "Invalid report type"
        }

    generation_time = round(
        time.time() - start_time,
        2
    )

    return {
        "success": True,
        "report_type": request.report_type,
        "report": report,
        "generation_time": generation_time,
        "error": None
    }

@app.post("/report/pdf")
def create_report_pdf(request: ReportRequest):
    start_time = time.time()
    report_type = (
        request.report_type
        .lower()
        .strip()
    )

    aliases = {
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

    report_type = aliases.get(
        report_type,
        report_type
    )

    report = generate_report(
        report_type
    )

    if report is None:
        return {
            "success": False,
            "file": None,
            "error": "Invalid report type"
        }

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        request.report_type.lower()
        + "_report_"
        + timestamp
        + ".pdf"
    )

    create_pdf(
        report,
        filename
    )

    generation_time = round(
        time.time() - start_time,
        2
    )

    return {
        "success": True,
        "report_type": request.report_type,
        "file": filename,
        "download_url": f"/download-report/{filename}",
        "generation_time": generation_time,
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
def dashboard():

    summary = {
        "customers": execute_query(
            "SELECT COUNT(*) FROM customers;"
        )[0][0],

        "calls": execute_query(
            "SELECT COUNT(*) FROM calls;"
        )[0][0],

        "services": execute_query(
            "SELECT COUNT(*) FROM services;"
        )[0][0],

        "surveys": execute_query(
            "SELECT COUNT(*) FROM surveys;"
        )[0][0]
    }

    complaints = execute_query("""
        SELECT
            issue_category,
            COUNT(*) AS complaints
        FROM calls
        WHERE call_type = 'Complaint'
        GROUP BY issue_category
        ORDER BY complaints DESC
        LIMIT 5;
    """)

    revenue = execute_query("""
        SELECT
            service_type,
            SUM(service_cost) AS revenue
        FROM services
        GROUP BY service_type
        ORDER BY revenue DESC
        LIMIT 5;
    """)

    ratings = execute_query("""
        SELECT
            c.branch,
            ROUND(AVG(s.customer_rating), 2)
        FROM surveys s
        JOIN services sv
            ON s.service_id = sv.service_id
        JOIN calls c
            ON sv.call_id = c.call_id
        GROUP BY c.branch
        ORDER BY 2 DESC
        LIMIT 10;
    """)

    return {
        "summary": summary,

        "complaints": [
            {
                "name": row[0],
                "value": row[1]
            }
            for row in complaints
        ],

        "revenue": [
            {
                "service": row[0],
                "revenue": row[1]
            }
            for row in revenue
        ],

        "ratings": [
            {
                "branch": row[0],
                "rating": row[1]
            }
            for row in ratings
        ]
    }
@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
@app.get("/version")
def version():

    return {
        "version": "1.0.0"
    }

@app.post("/report/custom")
def custom_report(
    request: CustomReportRequest
):

    report = generate_custom_report(
        request.question
    )

    return {
        "success": True,
        "question": request.question,
        "report": report,
        "error": None
    }