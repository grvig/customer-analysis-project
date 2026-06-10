import subprocess
import re
from database import execute_query
from config import REPORT_MODEL

def clean_text(text):

    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)
    text = text.replace('\u001b', '')
    text = text.strip()

    return text

def call_qwen(prompt):

    try:

        result = subprocess.run(
            [
                "ollama",
                "run",
                REPORT_MODEL
            ],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180
        )

        if result.returncode != 0:

            raise Exception(
                result.stderr
            )

        return clean_text(
            result.stdout.strip()
        )

    except Exception as e:

        raise Exception(
            f"Report model error: {str(e)}"
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
            ROUND(AVG(customer_rating), 2)
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
- Use only provided data.
- Do not invent numbers.
- Be professional.
- Do not include "Prepared By".
- Do not include signatures.
- Do not include contact information.
- Do not include dates.
- End the report after Recommendations.
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
- Use only provided data.
- Do not invent numbers.
- Be professional.
- Do not include "Prepared By".
- Do not include signatures.
- Do not include contact information.
- Do not include dates.
- End the report after Recommendations.
"""

    return call_qwen(prompt)

def generate_branch_report():

    branch_ratings = execute_query("""
        SELECT
            c.branch,
            ROUND(AVG(s.customer_rating), 2) AS rating
        FROM surveys s
        JOIN services sv
            ON s.service_id = sv.service_id
        JOIN calls c
            ON sv.call_id = c.call_id
        GROUP BY c.branch
        ORDER BY rating DESC;
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

    branch_complaints = execute_query("""
        SELECT
            branch,
            COUNT(*) AS complaints
        FROM calls
        WHERE call_type = 'Complaint'
        GROUP BY branch
        ORDER BY complaints DESC;
    """)

    prompt = f"""
You are a senior business analyst.

Generate a professional Branch Performance Report.

Data:

Branch Ratings:
{branch_ratings}

Branch Revenue:
{branch_revenue}

Branch Complaints:
{branch_complaints}

Report Format:

BRANCH PERFORMANCE REPORT

Executive Summary

Top Rated Branches

Revenue Performance

Complaint Analysis

Overall Branch Assessment

Recommendations

Rules:

- Use only provided data.
- Do not invent numbers.
- Be professional.
- Do not include "Prepared By".
- Do not include signatures.
- Do not include contact information.
- Do not include dates.
- End the report after Recommendations.
"""

    return call_qwen(prompt)

def generate_customer_satisfaction_report():

    average_rating = execute_query("""
        SELECT
            ROUND(
                AVG(customer_rating),
                2
            )
        FROM surveys;
    """)

    return_intent = execute_query("""
        SELECT
            will_return,
            COUNT(*)
        FROM surveys
        GROUP BY will_return;
    """)

    recommendation_intent = execute_query("""
        SELECT
            recommend_service,
            COUNT(*)
        FROM surveys
        GROUP BY recommend_service;
    """)

    feedback_samples = execute_query("""
        SELECT
            feedback
        FROM surveys
        LIMIT 20;
    """)

    prompt = f"""
You are a senior business analyst.

Generate a professional Customer Satisfaction Report.

Data:

Average Customer Rating:
{average_rating}

Will Return Analysis:
{return_intent}

Recommendation Analysis:
{recommendation_intent}

Customer Feedback Samples:
{feedback_samples}

Report Format:

CUSTOMER SATISFACTION REPORT

Executive Summary

Average Customer Rating

Return Intent Analysis

Recommendation Analysis

Feedback Insights

Recommendations

Rules:

- Use only provided data.
- Do not invent numbers.
- Be professional.
- Do not include "Prepared By".
- Do not include signatures.
- Do not include contact information.
- Do not include dates.
- End the report after Recommendations.
"""

    return call_qwen(prompt)

def generate_report(report_type):

    try:

        report_type = report_type.lower()

        if report_type == "complaint":
            return generate_complaint_report()

        elif report_type == "revenue":
            return generate_revenue_report()

        elif report_type == "branch":
            return generate_branch_report()

        elif report_type == "customer_satisfaction":
            return generate_customer_satisfaction_report()

        return None

    except Exception as e:

        raise Exception(
            f"Report generation failed: {str(e)}"
        )

if __name__ == "__main__":

    report = generate_report(
    "complaint"
)

    print("\n")
    print("=" * 60)
    print(report)
    print("=" * 60)