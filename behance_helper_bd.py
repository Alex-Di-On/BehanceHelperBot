from mysql.connector import connect, Error


def connect_database(id, url):
    try:
        with connect(host='31.31.196.38', user='u1726449_alex', password='vY9aQ3gX3x') as connection:
            print(connection)
            request_mysql = 'USE u1726449_default'
            request_insert = f"INSERT INTO behance_helper (client_id, url_interface) VALUES ('{id}', '{url}')"
            with connection.cursor() as cursor:
                cursor.execute(request_mysql)
                cursor.execute(request_insert)
                connection.commit()
    except Error as error:
        print(error)
