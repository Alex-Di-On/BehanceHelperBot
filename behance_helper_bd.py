from mysql.connector import connect, Error


class DataBase:
    """Database connection class."""

    connection = None
    cursor = None

    def __init__(self, host, user, password, database):
        """Initialisation of Class Object."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """Connection to the database."""
        try:
            self.connection = connect(host=self.host, user=self.user, password=self.password, database=self.database)
            return self.use_cursor()
        except Error as error:
            print(error)

    def use_cursor(self):
        """Cursor definition."""
        self.cursor = self.connection.cursor()


class DataBaseAction(DataBase):
    """Class for interacting with database."""

    request_insert = None
    request_reading = None

    def __init__(self, host, user, password, database, id, url):
        """Initialisation of Class Object."""
        super().__init__(host, user, password, database)
        self.id = id
        self.url = url

    def insert_data(self):
        """Writing data into database."""
        self.request_insert = f'''
        INSERT INTO behance_helper (
            client_id,
            url_interface)
        VALUES ('{self.id}', '{self.url}')
        '''
        try:
            self.cursor.execute(self.request_insert)
            self.connection.commit()
        except Error as error:
            print(error)

    def reading_data(self):
        """Reading data from database."""
        self.request_reading = f'''
        SELECT url_interface, id 
        FROM behance_helper
        WHERE client_id={self.id}
        '''
        try:
            self.cursor.execute(self.request_reading)
            self.connection.commit()
            result = self.cursor.fetchall()
            result_string = ' '.join(list(set([i[0] for i in result])))
            if len(result_string) == 0:
                return 'is empty.'
            return result_string
        except Error as error:
            print(error)




# def connect_database(id, url):
#     try:
#         with connect(host='31.31.196.38', user='u1726449_alex', password='vY9aQ3gX3x') as connection:
#             print(connection)
#             request_mysql = 'USE u1726449_default'
#             request_insert = f"INSERT INTO behance_helper (client_id, url_interface) VALUES ('{id}', '{url}')"
#             with connection.cursor() as cursor:
#                 cursor.execute(request_mysql)
#                 cursor.execute(request_insert)
#                 connection.commit()
#     except Error as error:
#         print(error)
#
#
# def get_url_history(id):
#     try:
#         with connect(host='31.31.196.38', user='u1726449_alex', password='vY9aQ3gX3x') as connection:
#             request_mysql = 'USE u1726449_default'
#             request_select = f"SELECT url_interface, id FROM behance_helper WHERE client_id={id}"
#             with connection.cursor() as cursor:
#                 cursor.execute(request_mysql)
#                 cursor.execute(request_select)
#                 result = cursor.fetchall()
#                 connection.commit()
#                 result_string = ' '.join(list(set([i[0] for i in result])))
#                 if len(result_string) == 0:
#                     return 'is empty.'
#                 return result_string
#     except Error as error:
#         print(error)
