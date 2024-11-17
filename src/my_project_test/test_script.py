import psycopg2
import re


DB_CONFIG = {"host": "localhost", "dbname": "postgres", "user": "postgres", "password": "11111", "port": 5432}


def execute_query(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


'''def get_table_columns(connection, table_name):
    query = f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [row[0] for row in cursor.fetchall()]
    return columns'''


def recreate_table_with_keep_data(connection, table_name, new_table_ddl):
    temp_table_name = f"{table_name}_2"

    create_temp_table_query = new_table_ddl.replace(table_name, temp_table_name)
    execute_query(connection, create_temp_table_query)
    print(f"Создана временная таблица {temp_table_name}")

    insert_data_query = f"""
        INSERT INTO {temp_table_name} 
        SELECT * FROM {table_name}
    """
    execute_query(connection, insert_data_query)
    print(f"Данные скопированы из {table_name} в {temp_table_name}")

    drop_old_table_query = f"DROP TABLE {table_name} CASCADE"
    execute_query(connection, drop_old_table_query)
    print(f"Таблица {table_name} удалена с CASCADE")

    # Разделяем имя таблицы и схему
    schema, original_table_name = table_name.split(".")
    rename_table_query = f"ALTER TABLE {temp_table_name} RENAME TO {original_table_name}"
    execute_query(connection, rename_table_query)
    print(f"Таблица {temp_table_name} переименована в {table_name}")

    restore_dependencies_query = f"SELECT bookings.restore_dependencies('{table_name}')"
    execute_query(connection, restore_dependencies_query)
    print(f"Зависимости для {table_name} восстановлены")


def process_sql_file(file_path):
    with open(file_path, "r") as file:
        sql_content = file.read()

    if "--<keep_data>" in sql_content:
        table_name_match = re.search(r"CREATE\s+TABLE\s+(\w+\.\w+)\s*\(", sql_content, re.IGNORECASE | re.DOTALL)
        if table_name_match:
            table_name = table_name_match.group(1)
            print(f"Обнаружена таблица для пересоздания: {table_name}")
            with psycopg2.connect(**DB_CONFIG) as conn:
                recreate_table_with_keep_data(conn, table_name, sql_content)
                # recreate_table_with_keep_data(conn, table_name, sql_content)
        else:
            print("Не удалось определить имя таблицы в SQL-файле.")
    else:
        print("Тег --<keep_data> не найден в файле.")


process_sql_file("src/my_project_test/migration_script.sql")
