import subprocess

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

    return result.stdout.strip()


if __name__ == "__main__":

    question = input("Enter question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)