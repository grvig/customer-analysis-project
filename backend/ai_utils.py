import subprocess
import re
from database import execute_custom_query

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

def generate_sql(question):

    with open(
        "schema_context.txt",
        "r",
        encoding="utf-8"
    ) as f:

        schema = f.read()

    prompt = f"""
{schema}

Analyze the question carefully.

Determine:

1. What business objective is being requested.
2. Which tables are required.
3. Which filters are required.
4. Which joins are required.
5. Whether complaint-related filtering is needed.

Then generate the PostgreSQL query.

Question:
{question}

SQL:
"""

    sql = call_qwen(prompt)

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql

def explain_results(question, rows):

    prompt = f"""
You are a business analytics assistant.

User Question:
{question}

Database Result:
{rows}

Provide a concise professional summary.

Rules:

- Do not mention SQL.
- Do not mention databases.
- Do not invent information.
- Only discuss information visible in the results.
- Keep response under 75 words.
"""

    answer = call_qwen(prompt)

    return clean_text(answer)

def ask_ai(question):

    sql = generate_sql(question)

    query_result = execute_custom_query(sql)

    if not query_result["success"]:

        return {
            "success": False,
            "sql": sql,
            "rows": [],
            "answer": None,
            "error": query_result["error"]
        }

    rows = query_result["rows"]

    answer = explain_results(
        question,
        rows
    )

    return {
        "success": True,
        "sql": sql,
        "rows": rows,
        "answer": answer,
        "error": None
    }