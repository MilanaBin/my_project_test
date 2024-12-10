import psycopg2
from psycopg2 import sql


def create_table(host, dbname, user, password, port, table_name, columns):
    """
    Создает таблицу в схеме bookings базы данных PostgreSQL.

    :param host: Хост базы данных
    :param dbname: Имя базы данных
    :param user: Имя пользователя базы данных
    :param password: Пароль пользователя
    :param port: Порт для подключения к базе данных
    :param table_name: Имя таблицы, которую нужно создать (без указания схемы)
    :param columns: Список столбцов с их типами данных (например: ["id SERIAL PRIMARY KEY", "name VARCHAR(255)"])
    """
    connection = None
    try:
        # Устанавливаем соединение с базой данных
        connection = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)

        # Создаем курсор
        cursor = connection.cursor()

        # Формируем SQL-запрос для создания таблицы
        create_table_query = sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS bookings.{table_name} (
                {columns}
            )
            """
        ).format(
            table_name=sql.Identifier(table_name), columns=sql.SQL(",").join(sql.SQL(column) for column in columns)
        )

        # Выполняем запрос
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Таблица bookings.{table_name} успешно создана.")

    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

    finally:
        # Закрываем соединение
        if connection:
            cursor.close()
            connection.close()


# Пример использования
if __name__ == "__main__":
    db_config = {"host": "localhost", "dbname": "postgres", "user": "postgres", "password": "11111", "port": 5432}

    table_name = "example_table"
    columns = ["id SERIAL PRIMARY KEY", "name VARCHAR(255) NOT NULL", "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"]

    create_table(
        host=db_config["host"],
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"],
        table_name=table_name,
        columns=columns,
    )
