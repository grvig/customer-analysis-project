import subprocess
import re
from database import execute_query
from config import REPORT_MODEL
from ai_utils import get_query_results
from database import execute_custom_query
from textwrap import dedent

def clean_text(text):

    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)
    text = text.replace('\u001b', '')
    text = text.strip()

    return text

def format_markdown_table(headers, rows):

    table = ""

    table += "| " + " | ".join(headers) + " |\n"

    table += "|" + "|".join(
        ["---"] * len(headers)
    ) + "|\n"

    for row in rows:
        formatted_row = []

        for value in row:
            if isinstance(value, int):
                formatted_row.append(f"{value:,}")

            elif isinstance(value, float):
                if value.is_integer():
                    formatted_row.append(f"{int(value):,}")
                else:
                    formatted_row.append(f"{value:,.2f}")

            else:
                formatted_row.append(str(value))

        table += (
            "| "
            + " | ".join(formatted_row)
            + " |\n"
        )

    print("\nTABLE DEBUG:")
    print(table)
    print()

    return table

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
    
    top_complaints_table = format_markdown_table(
        ["Category", "Complaints"],
        top_complaints
    )

    branch_table = format_markdown_table(
        ["Branch", "Complaints"],
        complaints_by_branch[:10]
    )

    priority_table = format_markdown_table(
        ["Category", "Complaints"],
        high_priority
    )

    prompt = f"""
You are a senior business analyst.

Top Complaint Categories:
{top_complaints}

Branch Complaint Volume:
{complaints_by_branch}

High Priority Complaints:
{high_priority}

Average Customer Rating:
{average_rating}

Write ONLY:

SUMMARY

- bullet
- bullet
- bullet

RECOMMENDATIONS

- bullet
- bullet
- bullet

Rules:

- Maximum 3 summary bullets.
- Maximum 3 recommendation bullets.
- Do not repeat numerical values.
- Do not repeat tables.
- Do not invent numbers.
- Do not speculate on causes.
- Keep response under 100 words.
- Do not repeat numerical values.
- Do not add currency symbols.
- Do not mention exact figures already shown in tables.
"""

    summary = call_qwen(prompt)

    report = f"""
# COMPLAINT ANALYSIS REPORT

## TOP COMPLAINT CATEGORIES

{top_complaints_table}

## BRANCH COMPLAINT VOLUME

{branch_table}

## HIGH PRIORITY ISSUES

{priority_table}

## CUSTOMER SATISFACTION

Average Rating: {average_rating[0][0]}

{summary}
"""

    return report


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
    top_services_table = format_markdown_table(
        ["Service Type", "Revenue"],
        top_services
    )

    branch_revenue_table = format_markdown_table(
        ["Branch", "Revenue"],
        branch_revenue
    )

    prompt = f"""
You are a senior business analyst.

Revenue By Service:
{top_services}

Revenue By Branch:
{branch_revenue}

Average Service Cost:
{avg_service_cost}

Write ONLY:

SUMMARY

- bullet
- bullet
- bullet

RECOMMENDATIONS

- bullet
- bullet
- bullet

Rules:

- Maximum 3 summary bullets.
- Maximum 3 recommendation bullets.
- Do not repeat numerical values.
- Do not repeat tables.
- Do not invent numbers.
- Keep response under 100 words.
- Do not repeat numerical values.
- Do not add currency symbols.
- Do not mention exact figures already shown in tables.
"""

    summary = call_qwen(prompt)

    report = f"""
# REVENUE ANALYSIS REPORT

## REVENUE BY SERVICE

{top_services_table}

## REVENUE BY BRANCH

{branch_revenue_table}

## AVERAGE SERVICE COST

{avg_service_cost[0][0]}

{summary}
"""

    return report

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

    ratings_table = format_markdown_table(
        ["Branch", "Rating"],
        branch_ratings
    )

    revenue_table = format_markdown_table(
        ["Branch", "Revenue"],
        branch_revenue
    )

    complaints_table = format_markdown_table(
        ["Branch", "Complaints"],
        branch_complaints
    )

    prompt = f"""
You are a senior business analyst.

Branch Ratings:
{branch_ratings}

Branch Revenue:
{branch_revenue}

Branch Complaints:
{branch_complaints}

Write ONLY:

SUMMARY

- bullet
- bullet
- bullet

RECOMMENDATIONS

- bullet
- bullet
- bullet

Rules:

- Maximum 3 summary bullets.
- Maximum 3 recommendation bullets.
- Do not repeat numerical values.
- Do not repeat tables.
- Do not invent numbers.
- Do not invent metrics.
- Do not invent percentages.
- Do not assume currency symbols.
- Do not speculate on causes.
- Keep response under 100 words.
- Do not repeat numerical values.
- Do not add currency symbols.
- Do not mention exact figures already shown in tables.
"""

    summary = call_qwen(prompt)

    report = f"""
#BRANCH PERFORMANCE REPORT

##BRANCH RATINGS

{ratings_table}

##BRANCH REVENUE

{revenue_table}

##BRANCH COMPLAINTS

{complaints_table}

{summary}
"""

    return report

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

    return_table = format_markdown_table(
        ["Will Return", "Count"],
        return_intent
    )

    recommendation_table = format_markdown_table(
        ["Recommend Service", "Count"],
        recommendation_intent
    )

    prompt = f"""
You are a senior business analyst.

Average Customer Rating:
{average_rating}

Will Return Analysis:
{return_intent}

Recommendation Analysis:
{recommendation_intent}

Write ONLY:

SUMMARY

- bullet
- bullet
- bullet

RECOMMENDATIONS

- bullet
- bullet
- bullet

Rules:

- Maximum 3 summary bullets.
- Maximum 3 recommendation bullets.
- Do not repeat numerical values.
- Do not repeat tables.
- Do not invent numbers.
- Do not invent metrics.
- Do not invent percentages.
- Do not assume currency symbols.
- Do not speculate on causes.
- Keep response under 100 words.
- Do not repeat numerical values.
- Do not add currency symbols.
- Do not mention exact figures already shown in tables.
"""

    summary = call_qwen(prompt)

    report = f"""
#CUSTOMER SATISFACTION REPORT

##AVERAGE CUSTOMER RATING

{average_rating[0][0]}

##RETURN INTENT

{return_table}

##RECOMMENDATION INTENT

{recommendation_table}

{summary}
"""

    return report

def generate_custom_report(question):
    
    question_lower = question.lower()

    if (
        "customers" in question_lower
        and "vehicles" in question_lower
        and "calls" in question_lower
        and "services" in question_lower
        and "surveys" in question_lower
    ):

        rows = execute_query("""
            SELECT
                (SELECT COUNT(*) FROM customers) AS customer_count,
                (SELECT COUNT(*) FROM vehicles) AS vehicle_count,
                (SELECT COUNT(*) FROM calls) AS call_count,
                (SELECT COUNT(*) FROM services) AS service_count,
                (SELECT COUNT(*) FROM surveys) AS survey_count;
        """)

        table = format_markdown_table(
            [
                "customer_count",
                "vehicle_count",
                "call_count",
                "service_count",
                "survey_count"
            ],
            rows
        )

        return dedent(f"""# CUSTOM REPORT

## USER REQUEST

{question}

## QUERY RESULTS

{table}
""")
    if (
        "average customer rating" in question_lower
        or "average rating" in question_lower
    ):
        rows = execute_query("""
        SELECT
            ROUND(
                AVG(customer_rating),
                2
            ) AS average_customer_rating
        FROM surveys;
    """)

        table = format_markdown_table(
            ["average_customer_rating"],
            rows
        )

        return dedent(f"""# CUSTOM REPORT

## USER REQUEST

{question}

## QUERY RESULTS

{table}
""")

    result = get_query_results(
        question
    )

    if not result["success"]:

        raise Exception(
            result["error"]
        )

    rows = result["rows"]
    columns = result["columns"]
    
    table = format_markdown_table(
        columns,
        rows
    )
    if len(rows) <= 5 and len(columns) <= 10:
        report = f"""
# CUSTOM REPORT

## USER REQUEST

{question}

## QUERY RESULTS

{table}
"""
        print("\nREPORT DEBUG:")
        print(repr(report))
        print()

        return report

    prompt = f"""
You are a senior business analyst.

User Request:
{question}

Data:
{table}

Write ONLY:

SUMMARY

- bullet
- bullet
- bullet

OBSERVATIONS

- bullet
- bullet
- bullet

Rules:

- Maximum 3 summary bullets.
- Maximum 3 recommendation bullets.
- Do not repeat all data values.
- Do not invent numbers.
- Do not invent metrics.
- Do not invent percentages.
- Do not assume currency symbols.
- Do not speculate on causes.
- Do not infer operational issues.
- Discuss only facts visible in the data.
- Keep response under 100 words.
- Do not repeat numerical values.
- Do not add currency symbols.
- Do not mention exact figures already shown in tables.
"""

    summary = call_qwen(prompt)

    report = f"""
# CUSTOM REPORT

## USER REQUEST

{question}

## QUERY RESULTS

{table}

{summary}
"""
    print("\nREPORT DEBUG:")
    print(repr(report))
    print()
    return report
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
        "revenue"
    )

    print("\n")
    print("=" * 60)
    print(report)
    print("=" * 60)