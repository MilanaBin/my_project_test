import psycopg2
import re

DB_CONFIG = {
    "host": "localhost",
    "dbname": "postgres",
    "user": "postgres",
    "password": "11111",
    "port": 5432,
    "options": "-c search_path=bookings",
}


def execute_query(connection, query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            print(f"Выполнен запрос: {query}")
    except Exception as e:
        print(f"Ошибка выполнения запроса: {query}\nОшибка: {e}")
        raise


def get_columns(connection, table_name):
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
    """
    schema, table = table_name.split(".")
    with connection.cursor() as cursor:
        cursor.execute(query, (schema, table))
        return [row[0] for row in cursor.fetchall()]


def recreate_table_with_keep_data(connection, table_name, new_table_ddl):
    schema, original_table_name = table_name.split(".")
    temp_table_name = f"{original_table_name}_2"
    temp_full_name = f"{schema}.{temp_table_name}"

    # Создание временной таблицы
    create_temp_table_query = new_table_ddl.replace(table_name, temp_full_name)
    execute_query(connection, create_temp_table_query)
    print(f"Создана временная таблица {temp_full_name}")

    # Получение списка колонок
    old_columns = get_columns(connection, table_name)
    new_columns = get_columns(connection, temp_full_name)

    # Найти пересечение столбцов
    common_columns = set(old_columns) & set(new_columns)
    if not common_columns:
        raise ValueError("Нет общих колонок между старой и новой таблицами!")

    common_columns = list(common_columns)
    column_list = ", ".join(common_columns)

    # Копирование данных
    insert_data_query = f"""
        INSERT INTO {temp_full_name} ({column_list})
        SELECT {column_list} FROM {table_name}
    """
    execute_query(connection, insert_data_query)
    print(f"Данные скопированы из {table_name} в {temp_full_name}")

    # Удаление старой таблицы
    drop_old_table_query = f"DROP TABLE {table_name} CASCADE"
    execute_query(connection, drop_old_table_query)
    print(f"Таблица {table_name} удалена с CASCADE")

    # Переименование временной таблицы
    rename_table_query = f"ALTER TABLE {temp_full_name} RENAME TO {original_table_name}"
    execute_query(connection, rename_table_query)
    print(f"Таблица {temp_full_name} переименована в {table_name}")

    # Восстановление зависимостей
    restore_dependencies_query = f"SELECT bookings.restore_dependencies('{table_name}')"
    execute_query(connection, restore_dependencies_query)
    print(f"Зависимости для {table_name} восстановлены")


def process_sql_file(file_path):
    try:
        with open(file_path, "r") as file:
            sql_content = file.read()

        if "--<keep_data>" in sql_content:
            table_name_match = re.search(r"CREATE\s+TABLE\s+(\w+\.\w+)\s*\(", sql_content, re.IGNORECASE | re.DOTALL)
            if table_name_match:
                table_name = table_name_match.group(1)
                print(f"Обнаружена таблица для пересоздания: {table_name}")

                # Соединение с базой данных
                with psycopg2.connect(**DB_CONFIG) as conn:
                    recreate_table_with_keep_data(conn, table_name, sql_content)
            else:
                print("Не удалось определить имя таблицы в SQL-файле.")
        else:
            print("Тег --<keep_data> не найден в файле.")
    except Exception as e:
        print(f"Ошибка обработки файла {file_path}: {e}")


# Путь к SQL-файлу для тестирования
process_sql_file("src/my_project_test/migration_script.sql")
