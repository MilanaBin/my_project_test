import psycopg2


DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "11111"
DB_NAME = "postgres"


try:
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)
    print("Connected to the database")
except Exception as e:
    print(f"Failed to connect to database: {e}")
