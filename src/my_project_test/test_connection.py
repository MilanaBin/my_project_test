import psycopg2
import os


def main():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        print("✅ Successfully connected to PostgreSQL")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
