import subprocess
from config import MODEL_NAME
import re
from database import execute_custom_query
import time
MAX_SQL_RETRIES = 1

def clean_text(text):

    text = re.sub(
        r'\x1b\[[0-9;]*[A-Za-z]',
        '',
        text
    )

    text = text.replace(
        '\u001b',
        ''
    )

    text = text.strip()
    
    lines = text.split("\n")
    fixed_lines = []

    i = 0

    while i < len(lines):

        current = lines[i].strip()

        if i < len(lines) - 1:

            nxt = lines[i + 1].strip()

            current_words = current.split()

            next_words = nxt.split()

            if (
                current_words
                and next_words
                and len(current_words[-1]) >= 2
                and next_words[0].startswith(
                    current_words[-1]
                )
            ):
                current_words[-1] = next_words[0]

                next_words = next_words[1:]

                current = " ".join(current_words)
                nxt = " ".join(next_words)

                fixed_lines.append(current)

                if nxt:
                    fixed_lines.append(nxt)

                i += 2
                continue

        fixed_lines.append(current)
        i += 1

    text = "\n".join(fixed_lines)

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if cleaned_lines:

            previous = cleaned_lines[-1]

            if (
                len(previous) > 3
                and line.startswith(previous)
            ):
                cleaned_lines[-1] = line
                continue

        cleaned_lines.append(line)

    words = text.split()
    cleaned_words = []

    i = 0

    while i < len(words):

        if (
            i < len(words) - 1
            and len(words[i]) >= 4
            and words[i + 1].startswith(words[i])
        ):
            cleaned_words.append(
                words[i + 1]
            )
            i += 2
            continue

        cleaned_words.append(
            words[i]
        )

        i += 1

    text = " ".join(cleaned_words)

    return "\n".join(cleaned_lines)

def call_qwen(prompt):

    try:

        result = subprocess.run(
            [
                "ollama",
                "run",
                MODEL_NAME
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
            f"AI model error: {str(e)}"
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

Convert the following question into a PostgreSQL SELECT query.

Return ONLY SQL.

Do not explain.

Do not use markdown.

Do not include comments.

Question:
{question}

SQL:
"""

    response = call_qwen(prompt)

    print("\nRAW MODEL RESPONSE:")
    print(response)
    print()

    sql = response

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    sql = sql.replace("\n", " ")
    sql = sql.replace("\r", " ")
    sql = " ".join(sql.split())
    
    print("\nGENERATED SQL:")
    print(sql)
    print()

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
- Do not assume currency symbols.
- Do not infer units, currencies, percentages, or ratings.
- Do not create numbered lists.
- Summarize the key insight only.
- Keep response under 50 words.
- Use professional business language.
- Mention only the most important findings.
- Avoid repeating all rows from the result.
- If many rows are returned, summarize overall trends.
"""

    answer = call_qwen(prompt)

    return clean_text(answer)

def regenerate_sql(
    question,
    failed_sql,
    error_message
):

    with open(
        "schema_context.txt",
        "r",
        encoding="utf-8"
    ) as f:

        schema = f.read()

    prompt = f"""
{schema}

The previous SQL failed.

Question:
{question}

Failed SQL:
{failed_sql}

Database Error:
{error_message}

Generate a corrected PostgreSQL SELECT query.

Return ONLY SQL.
"""

    sql = call_qwen(prompt)

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    sql = sql.replace("\n", " ")
    sql = sql.replace("\r", " ")
    sql = " ".join(sql.split())


    return sql

def get_query_results(question):

    sql = generate_sql(
        question
    )
    print("\n========== GENERATED SQL ==========")
    print(sql)
    print("===================================\n")

    query_result = execute_custom_query(
        sql
    )

    for _ in range(MAX_SQL_RETRIES):

        if query_result["success"]:
            break

        sql = regenerate_sql(
            question,
            sql,
            query_result["error"]
        )

        query_result = execute_custom_query(
            sql
        )

    if not query_result["success"]:

        return {
            "success": False,
            "sql": sql,
            "rows": [],
            "error": query_result["error"]
        }

    return {
        "success": True,
        "sql": sql,
        "columns": query_result["columns"],
        "rows": query_result["rows"],
        "error": None
    }

def ask_ai(question):
    start_time = time.time()

    try:

        sql = generate_sql(question)

        query_result = execute_custom_query(
            sql
        )

        for _ in range(MAX_SQL_RETRIES):
            if query_result["success"]:
                break

            sql = regenerate_sql(
                question,
                sql,
                query_result["error"]
            )
            query_result = execute_custom_query(sql)
            print("\n========== QUERY RESULT ==========")
            print(query_result)
            print("==================================\n")


        if not query_result["success"]:
            execution_time = round(
                time.time() - start_time,
                2
            )

            return {
                "success": False,
                "sql": sql,
                "rows": [],
                "answer": None,
                "execution_time": execution_time,
                "error": query_result["error"]
            }

        rows = query_result["rows"]

        answer = explain_results(
            question,
            rows
        )
        execution_time = round(
            time.time() - start_time,
            2
        )

        return {
            "success": True,
            "sql": sql,
            "rows": rows,
            "answer": answer,
            "execution_time": execution_time,
            "error": None
        }

    except Exception as e:
        execution_time = round(
        time.time() - start_time,
        2
    )
        return {
            "success": False,
            "sql": None,
            "rows": [],
            "answer": None,
            "execution_time": execution_time,
            "error": str(e)
        }