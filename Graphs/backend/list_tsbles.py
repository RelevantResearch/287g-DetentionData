import psycopg2

# Connection parameters
host = "localhost"
database = "287g"
user = "postgres"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(host=host, database=database, user=user)
    cur = conn.cursor()

    # Query to list all tables in public schema
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        ORDER BY table_name;
    """)

    tables = cur.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"- {table[0]}")

    # Close connection
    cur.close()
    conn.close()

except Exception as e:
    print("Error connecting to database:", e)
