import psycopg2


def recreate_table_with_keep_data(schema, table_name):
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="11111", host="localhost", port=5432)
    cursor = connection.cursor()

    # cursor.execute(f"SELECT * from {schema}.{table_name};")
    cursor.execute(f"""
            CREATE TABLE {schema}.{table_name} (
                column1 varchar,
                column2 numeric
            )
        """)

    connection.commit()
    cursor.close()
    connection.close()


# Запуск функции с параметрами
recreate_table_with_keep_data("bookings", "flights2")
