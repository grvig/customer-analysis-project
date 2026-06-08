import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="customer_analysis",
        user="postgres",
        password="134679",
        port="5432"
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

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query)

    try:
        rows = cur.fetchall()
    except:
        rows = []

    cur.close()
    conn.close()

    return rows