import psycopg2
from psycopg2 import OperationalError

# Конфигурация подключения
db_config = {
    "host": "localhost",
    "dbname": "postgres",
    "user": "postgres",
    "password": "11111",
    "port": 5432,
}


def check_connection(config):
    try:
        # Подключение к базе данных PostgreSQL
        connection = psycopg2.connect(**config)

        # Проверка успешного подключения
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        print("Connection successful")

        # Закрытие соединения
        cursor.close()
        connection.close()
    except OperationalError as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    check_connection(db_config)
