import psycopg2
from psycopg2 import sql


def check_connection(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user")
            db_info = cursor.fetchone()
            print(f"Connected to database: {db_info[0]} as user: {db_info[1]}")
    except Exception as e:
        print(f"Error checking connection: {e}")
        raise


def create_table(host, dbname, user, password, port, table_name, columns):
    connection = None
    try:
        connection = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)

        check_connection(connection)

        with connection.cursor() as cursor:
            create_table_query = sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS bookings.{table_name} (
                    {columns}
                )
                """
            ).format(
                table_name=sql.Identifier(table_name), columns=sql.SQL(",").join(sql.SQL(column) for column in columns)
            )
            cursor.execute(create_table_query)
            connection.commit()
            print(f"Table bookings.{table_name} created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "dbname": "postgres",
        "user": "postgres",
        "password": "your_password",
        "port": 5432,
    }

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
