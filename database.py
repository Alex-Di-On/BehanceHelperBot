from mysql.connector import connect, Error


class DataBase:
    """Database connection class."""

    connection = None
    cursor = None
    request_data_insert = None
    request_reading_last_note = None
    request_reading_history = None
    request_emoji_flag = None
    request_all_countries = None

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

    def insert_data(self, id, url):
        """Insert data into database."""
        self.request_data_insert = f'''
        INSERT INTO behance_helper (
            client_id,
            url_interface)
        VALUES ('{id}', '{url}')
        '''
        try:
            self.cursor.execute(self.request_data_insert)
            self.connection.commit()
        except Error as error:
            print(error)

    def reading_last_note(self, id):
        """Return last note from database by client_id."""
        self.request_reading_last_note = f'''
        SELECT
            url_interface, id
        FROM
            behance_helper
        WHERE client_id = '{id}'
        ORDER BY id
        DESC LIMIT 1
        '''
        try:
            self.cursor.execute(self.request_reading_last_note)
            result = self.cursor.fetchall()
            self.connection.commit()
            return result[0][0].lower()
        except Error as error:
            print(error)

    def reading_history(self, id):
        """Return info (set urls) from database."""
        self.request_reading_history = f'''
        SELECT
            url_interface, id
        FROM
            behance_helper
        WHERE
            client_id='{id}'
        '''
        try:
            self.cursor.execute(self.request_reading_history)
            result = self.cursor.fetchall()
            self.connection.commit()
            result_string = ' '.join(list(set([i[0].lower() for i in result])))
            if len(result_string) == 0:
                return 'is empty.'
            return result_string
        except Error as error:
            print(error)

    def reading_all_countries(self):
        """Return array of all countries from database."""
        self.request_all_countries = f'''
        SELECT
            country, id
        FROM
            emoji_flags
        '''
        try:
            self.cursor.execute(self.request_all_countries)
            result = self.cursor.fetchall()
            self.connection.commit()
            countries = [i[0] for i in result]
            return countries
        except Error as error:
            print(error)

    def reading_emoji_flag(self, location):
        """Return emoji flag from database by location."""
        self.request_emoji_flag = f'''
        SELECT
            flag, id
        FROM
            emoji_flags
        WHERE country = '{location}'
        '''
        try:
            self.cursor.execute(self.request_emoji_flag)
            result = self.cursor.fetchall()
            self.connection.commit()
            return result[0][0].lower()
        except Error as error:
            print(error)
