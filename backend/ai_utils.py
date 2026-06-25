import subprocess
from config import MODEL_NAME
import re
from database import execute_custom_query
import time
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

MAX_SQL_RETRIES = 3

def clean_generated_sql(sql):

    sql = re.sub(
        r"\bA\s+AS\b",
        "AS",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"\bDESCLIMIT\b",
        "DESC LIMIT",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"\bLIMI\s+LIMIT\b",
        "LIMIT",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"\bDE\s+DESC\b",
        "DESC",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"\bAS\s+AS\b",
        "AS",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"\bD\s+DESC\b",
        "DESC",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"\b(\w+)\s+\1\b",
        r"\1",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"\s+",
        " ",
        sql
    )
    
    sql = re.sub(
        r"\bPARTITION\s+\w+\s+BY\b",
        "PARTITION BY",
        sql,
        flags=re.IGNORECASE
    )
    
    sql = re.sub(
        r"\bJOIN\s+\w+\s+(services|calls|vehicles|customers|agents|surveys)\b",
        r"JOIN \1",
        sql,
        flags=re.IGNORECASE
    )
    
    sql = re.sub(
        r"\b(\w+)\s+\1\.",
        r"\1.",
        sql,
        flags=re.IGNORECASE
    )
    
    sql = re.sub(
        r"\b(\w+)\s+\1_(\w+)\b",
        r"\1_\2",
        sql,
        flags=re.IGNORECASE
    )
    
    sql = re.sub(
        r"\bA\s+AND\b",
        "AND",
        sql,
        flags=re.IGNORECASE
    )

    return sql.strip()

def log_sql(
    question,
    generated_sql,
    final_sql,
    success,
    error,
    retry_count,
    validation_passed,
    validation_errors
):

    try:

        with open(
            "sql_history.txt",
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n" +
                "=" * 60 +
                "\n"
            )

            f.write(
                f"Timestamp: "
                f"{datetime.now()}\n\n"
            )

            f.write(
                f"Question:\n"
                f"{question}\n\n"
            )

            f.write(
                f"Generated SQL:\n"
                f"{generated_sql}\n\n"
            )

            f.write(
                f"Final SQL:\n"
                f"{final_sql}\n\n"
            )
            
            f.write(
                f"Validation Passed:\n"
                f"{validation_passed}\n\n"
            )

            f.write(
                f"Validation Errors:\n"
                f"{validation_errors}\n\n"
            )
            
            f.write(
                f"Retries:\n"
                f"{retry_count}\n\n"
            )

            f.write(
                f"Success:\n"
                f"{success}\n\n"
            )

            f.write(
                f"Error:\n"
                f"{error}\n"
            )

    except Exception as e:

        logger.error(f"Logging error: {e}")
        
def validate_sql(sql):

    errors = []

    invalid_patterns = [
        ("services.customer_rating",
         "customer_rating exists only in surveys"),

        ("calls.service_id",
         "calls does not contain service_id"),

        ("calls.service_cost",
         "service_cost exists only in services"),

        ("services.branch",
         "branch exists only in calls"),

        ("services.survey_id",
         "survey_id exists only in surveys")
    ]

    for pattern, message in invalid_patterns:

        if pattern.lower() in sql.lower():

            errors.append(message)

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

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

IMPORTANT:

customer_rating exists ONLY in surveys.

service_cost exists ONLY in services.

branch exists ONLY in calls.

Revenue by branch requires:

If ratings are requested:

ALWAYS use surveys.customer_rating.

NEVER use services.customer_rating.

NEVER use calls.customer_rating.

services
JOIN calls
ON services.call_id = calls.call_id

Ratings by branch requires:

surveys
JOIN services
ON surveys.service_id = services.service_id

JOIN calls
ON services.call_id = calls.call_id

Convert the following question into a PostgreSQL SELECT query.

Return ONLY SQL.

Question:
{question}

SQL:
"""

    response = call_qwen(prompt)

    logger.debug(f"Raw model response: {response}")

    sql = response

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    sql = sql.replace("\n", " ")
    sql = sql.replace("\r", " ")
    sql = " ".join(sql.split())
    
    sql = clean_generated_sql(sql)
    
    logger.debug(f"Generated SQL: {sql}")

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

IMPORTANT:

Fix ONLY the reported error.

Do not rewrite the entire query.

Keep all correct joins.

Keep all correct filters.

Keep all correct aggregations.

If the error says a column does not exist,
replace only that column.

If the error says a table alias is wrong,
replace only that alias.

Return ONLY SQL.
"""

    sql = call_qwen(prompt)

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    sql = sql.replace("\n", " ")
    sql = sql.replace("\r", " ")
    sql = " ".join(sql.split())
    
    sql = clean_generated_sql(sql)

    logger.debug(f"Regenerated SQL: {sql}")

    return sql

def regenerate_empty_result_sql(
    question,
    previous_sql
):

    with open(
        "schema_context.txt",
        "r",
        encoding="utf-8"
    ) as f:

        schema = f.read()

    prompt = f"""
{schema}

The SQL query executed successfully.

However it returned ZERO rows.

User Question:
{question}

Previous SQL:
{previous_sql}

Generate a less restrictive PostgreSQL query.

Keep the same business intent.

Return ONLY SQL.
"""

    sql = call_qwen(prompt)

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    sql = sql.replace("\n", " ")
    sql = sql.replace("\r", " ")
    sql = " ".join(sql.split())
    
    sql = clean_generated_sql(sql)

    return sql

def get_query_results(question):

    sql = generate_sql(
        question
    )
    logger.debug(f"Generated SQL (get_query_results): {sql}")

    query_result = execute_custom_query(
        sql
    )

    if (
        query_result["success"]
        and len(query_result["rows"]) == 0
    ):

        logger.warning("Empty result detected, retrying with less restrictive query")

        sql = regenerate_empty_result_sql(
            question,
            sql
        )

        logger.debug(f"Empty result retry SQL: {sql}")

        query_result = execute_custom_query(
            sql
        )

    for attempt in range(MAX_SQL_RETRIES):

        if query_result["success"]:
            break

        logger.warning(f"SQL retry {attempt + 1}: {query_result['error']}")

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
    
    logger.debug(f"Final SQL success: {sql}")

    return {
        "success": True,
        "sql": sql,
        "columns": query_result["columns"],
        "rows": query_result["rows"],
        "error": None
    }

def ask_ai(question):
    start_time = time.time()
    retry_count = 0

    try:

        generated_sql = generate_sql(question)

        sql = generated_sql

        validation = validate_sql(sql)
        
        validation_passed = validation["valid"]

        validation_errors = validation["errors"]

        if not validation["valid"]:

            logger.warning(f"SQL validation failed: {validation['errors']}")

            sql = regenerate_sql(
                question,
                sql,
                ", ".join(
                    validation["errors"]
                )
            )

        query_result = execute_custom_query(
            sql
        )

        for attempt in range(MAX_SQL_RETRIES):
            if query_result["success"]:
                break
            retry_count += 1
            sql = regenerate_sql(
                question,
                sql,
                query_result["error"]
            )
            query_result = execute_custom_query(sql)
            logger.debug(f"Query result after retry: {query_result}")

        if not query_result["success"]:
            execution_time = round(
                time.time() - start_time,
                2
            )
            
            log_sql(
                question,
                generated_sql,
                sql,
                False,
                query_result["error"],
                retry_count,
                validation_passed,
                validation_errors
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
        
        log_sql(
            question,
            generated_sql,
            sql,
            True,
            None,
            retry_count,
            validation_passed,
            validation_errors
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