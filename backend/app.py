from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database import execute_query, execute_custom_query
from ai_utils import ask_ai
from report_generator import generate_report
from pdf_generator import create_pdf
import time

app = FastAPI()

class QueryRequest(BaseModel):
    sql: str

class AskRequest(BaseModel):
    question: str

class ReportRequest(BaseModel):
    report_type: str

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

    report = generate_report(
        request.report_type
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

    report = generate_report(
        request.report_type
    )

    if report is None:

        return {
            "success": False,
            "file": None,
            "error": "Invalid report type"
        }

    filename = (
        request.report_type.lower()
        + "_report.pdf"
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