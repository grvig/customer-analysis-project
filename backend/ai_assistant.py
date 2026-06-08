import subprocess
from database import execute_custom_query

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

    return result.stdout.strip()

def generate_sql(question):

    with open("schema_context.txt", "r", encoding="utf-8") as f:
        schema = f.read()

    prompt = f"""
{schema}

Question:
{question}

SQL:
"""

    sql = call_qwen(prompt)

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql

def explain_results(question, sql, rows):

    prompt = f"""
You are a business analytics assistant.

User Question:
{question}

SQL Used:
{sql}

Database Result:
{rows}

Provide a short professional summary of the results.

Rules:
- Do not mention SQL.
- Do not mention databases.
- Write like a business analyst.
- Keep it under 100 words.
"""

    return call_qwen(prompt)

if __name__ == "__main__":

    question = input("Enter question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)

    rows = execute_custom_query(sql)

    print("\nDatabase Result:\n")
    print(rows)

    answer = explain_results(
        question,
        sql,
        rows
    )

    print("\nAI Summary:\n")
    print(answer)