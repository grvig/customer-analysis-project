import subprocess
import re
from database import execute_query

def clean_text(text):

    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)
    text = text.replace('\u001b', '')
    text = text.strip()

    return text

def call_qwen(prompt):

    result = subprocess.run(
        [
            "ollama",
            "run",
            "qwen2.5-coder:7b"
        ],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    return clean_text(
        result.stdout.strip()
    )

def generate_complaint_report():

    top_complaints = execute_query("""
        SELECT
            issue_category,
            COUNT(*) AS complaints
        FROM calls
        WHERE call_type = 'Complaint'
        GROUP BY issue_category
        ORDER BY complaints DESC
        LIMIT 10;
    """)

    complaints_by_branch = execute_query("""
        SELECT
            branch,
            COUNT(*) AS complaints
        FROM calls
        WHERE call_type = 'Complaint'
        GROUP BY branch
        ORDER BY complaints DESC;
    """)

    high_priority = execute_query("""
        SELECT
            issue_category,
            COUNT(*) AS complaints
        FROM calls
        WHERE
            call_type = 'Complaint'
            AND priority = 'High'
        GROUP BY issue_category
        ORDER BY complaints DESC;
    """)

    average_rating = execute_query("""
        SELECT
            ROUND(
                AVG(customer_rating),
                2
            )
        FROM surveys;
    """)

    prompt = f"""
You are a senior business analyst.

Generate a professional Complaint Analysis Report.

Data:

Top Complaint Categories:
{top_complaints}

Complaint Volume By Branch:
{complaints_by_branch}

High Priority Complaints:
{high_priority}

Average Customer Rating:
{average_rating}

Report Format:

COMPLAINT ANALYSIS REPORT

Executive Summary

Top Complaint Categories

Branch Analysis

High Priority Issues

Customer Satisfaction

Recommendations

Rules:

- Use only the provided data.
- Do not invent numbers.
- Be professional.
- Keep the report under 400 words.
"""

    return call_qwen(prompt)

def generate_revenue_report():

    top_services = execute_query("""
        SELECT
            service_type,
            SUM(service_cost) AS revenue
        FROM services
        GROUP BY service_type
        ORDER BY revenue DESC
        LIMIT 10;
    """)

    branch_revenue = execute_query("""
        SELECT
            c.branch,
            SUM(s.service_cost) AS revenue
        FROM services s
        JOIN calls c
            ON s.call_id = c.call_id
        GROUP BY c.branch
        ORDER BY revenue DESC;
    """)

    avg_service_cost = execute_query("""
        SELECT
            ROUND(AVG(service_cost),2)
        FROM services;
    """)

    prompt = f"""
You are a senior business analyst.

Generate a professional Revenue Analysis Report.

Data:

Top Revenue Services:
{top_services}

Revenue By Branch:
{branch_revenue}

Average Service Cost:
{avg_service_cost}

Report Format:

REVENUE ANALYSIS REPORT

Executive Summary

Top Revenue Services

Branch Revenue Analysis

Average Service Cost

Recommendations

Rules:

- Use only the provided data.
- Do not invent numbers.
- Be professional.
- Keep the report under 400 words.
"""

    return call_qwen(prompt)

if __name__ == "__main__":

    report = generate_revenue_report()

    print("\n")
    print("=" * 60)
    print(report)
    print("=" * 60)