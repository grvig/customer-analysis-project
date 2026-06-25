import psycopg2
import psycopg2.errors
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "customer_analysis"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

def execute_query(query):

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    except psycopg2.OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise

    except psycopg2.DatabaseError as e:
        logger.error(f"Database query error: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def _apply_limit(query, limit=500):
    if "LIMIT" not in query.upper():
        query = query.rstrip().rstrip(";") + f" LIMIT {limit};"
    return query

def execute_custom_query(query):

    conn = None
    cur = None

    try:
        query = _apply_limit(query)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []

        return {
            "success": True,
            "columns": columns,
            "rows": rows,
            "error": None
        }

    except psycopg2.OperationalError as e:
        logger.error(f"Database connection error: {e}")
        return {
            "success": False,
            "rows": [],
            "error": f"Database connection error: {str(e)}"
        }

    except psycopg2.DatabaseError as e:
        logger.error(f"Database query error: {e}")
        return {
            "success": False,
            "rows": [],
            "error": f"Database query error: {str(e)}"
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "success": False,
            "rows": [],
            "error": str(e)
        }

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
