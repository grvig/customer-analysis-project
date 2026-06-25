import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "customer_analysis"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

def execute_query(query):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

def execute_custom_query(query):

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(query)

        try:
            rows = cur.fetchall()
            columns = [
                desc[0]
                for desc in cur.description
            ]
        except Exception:
            rows = []
            columns = []

        cur.close()
        conn.close()

        return {
            "success": True,
            "columns": columns,
            "rows": rows,
            "error": None
        }

    except Exception as e:

        return {
            "success": False,
            "rows": [],
            "error": str(e)
        }