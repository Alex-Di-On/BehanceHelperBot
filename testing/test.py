from mysql.connector import connect, Error


class DataBase:
    """Database connection class."""

    connection = None
    cursor = None
    request_insert = None
    request_reading = None
    request_mysql = 'USE u1726449_default'

    def __init__(self, host, user, password, database, id, url):
        """Initialisation of Class Object."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.id = id
        self.url = url

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

    def insert_data(self):
        """Writing data into database."""
        self.request_insert = f'''
        INSERT INTO behance_helper (client_id, url_interface)
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
            result = self.cursor.fetchall()
            self.connection.commit()
            result_string = ' '.join(list(set([i[0] for i in result])))
            if len(result_string) == 0:
                return 'is empty.'
            return result_string
        except Error as error:
            print(error)


db = DataBase('31.31.196.38', 'u1726449_alex', 'eY4vT5pM6m', 'u1726449_default', 1172947980, 'monster')
db.connect()
db.use_cursor()
print(db.reading_data())

