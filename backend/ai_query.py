import subprocess
from database import execute_custom_query

def generate_sql(question):

    with open("schema_context.txt", "r", encoding="utf-8") as f:
        schema = f.read()

    prompt = f"""
{schema}

Question:
{question}

SQL:
"""

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

    sql = result.stdout.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql

if __name__ == "__main__":

    question = input("Enter question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)

    try:

        rows = execute_custom_query(sql)

        print("\nDatabase Result:\n")
        print(rows)

    except Exception as e:

        print("\nExecution Error:\n")
        print(e)