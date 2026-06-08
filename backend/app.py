from fastapi import FastAPI
from pydantic import BaseModel
from database import execute_query, execute_custom_query

app = FastAPI()

class QueryRequest(BaseModel):
    sql: str

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

@app.get("/top-complaints")
def top_complaints():

    rows = execute_query("""
        SELECT
            issue_category,
            COUNT(*) AS complaints
        FROM calls
        WHERE call_type = 'Complaint'
        GROUP BY issue_category
        ORDER BY complaints DESC
        LIMIT 10;
    """)

    result = []

    for row in rows:
        result.append({
            "issue_category": row[0],
            "complaints": row[1]
        })

    return result

@app.get("/branch-ratings")
def branch_ratings():

    rows = execute_query("""
        SELECT
            c.branch,
            ROUND(
                AVG(s.customer_rating),
                2
            ) AS avg_rating
        FROM surveys s
        JOIN services sv
            ON s.service_id = sv.service_id
        JOIN calls c
            ON sv.call_id = c.call_id
        GROUP BY c.branch
        ORDER BY avg_rating DESC;
    """)

    result = []

    for row in rows:
        result.append({
            "branch": row[0],
            "average_rating": float(row[1])
        })

    return result

@app.get("/service-revenue")
def service_revenue():

    rows = execute_query("""
        SELECT
            service_type,
            SUM(service_cost) AS revenue
        FROM services
        GROUP BY service_type
        ORDER BY revenue DESC;
    """)

    result = []

    for row in rows:
        result.append({
            "service_type": row[0],
            "revenue": int(row[1])
        })

    return result

@app.get("/agent-performance")
def agent_performance():

    rows = execute_query("""
        SELECT
            a.agent_name,
            COUNT(*) AS calls_handled
        FROM calls c
        JOIN agents a
            ON c.agent_id = a.agent_id
        GROUP BY a.agent_name
        ORDER BY calls_handled DESC
        LIMIT 10;
    """)

    result = []

    for row in rows:
        result.append({
            "agent_name": row[0],
            "calls_handled": row[1]
        })

    return result

@app.post("/query")
def run_query(request: QueryRequest):

    rows = execute_custom_query(
        request.sql
    )

    return {
        "rows": rows
    }