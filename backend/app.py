from fastapi import FastAPI
from pydantic import BaseModel
from database import execute_query, execute_custom_query
from ai_utils import ask_ai
from report_generator import (
    generate_complaint_report,
    generate_revenue_report,
    generate_branch_report,
    generate_customer_satisfaction_report
)

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

    report_type = request.report_type.lower()

    if report_type == "complaint":

        report = generate_complaint_report()

    elif report_type == "revenue":

        report = generate_revenue_report()

    elif report_type == "branch":

        report = generate_branch_report()

    elif report_type == "customer_satisfaction":

        report = generate_customer_satisfaction_report()

    else:

        return {
            "success": False,
            "report": None,
            "error": "Invalid report type"
        }

    return {
        "success": True,
        "report_type": report_type,
        "report": report,
        "error": None
    }