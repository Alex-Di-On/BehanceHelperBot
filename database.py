from mysql.connector import connect, Error
from config import configuration


class MetaSingleton(type):
    """Metaclass singleton."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Return _instances."""
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBase(metaclass=MetaSingleton):
    """Database connection class."""

    __host = configuration['host']
    __user = configuration['user']
    __password = configuration['password']
    __database = configuration['database']
    __connection = None
    __cursor = None

    def connection(self) -> None:
        """Connection to database."""
        if self.__connection is None:
            self.__connection = connect(host=self.__host, user=self.__user,
                                        password=self.__password, database=self.__database)
            self.__cursor = self.__connection.cursor()

    def call_database(self, request: str) -> None:
        """Sending query to database."""
        self.__cursor.execute(request)
        self.__connection.commit()

    def insert_data(self, id: int, url: str) -> str:
        """Insert data into database."""
        return f'''
        INSERT INTO behance_helper (
            client_id,
            url_interface)
        VALUES ('{id}', '{url}')
        '''









    #
    #
    # def reading_last_note(self, id):
    #     """Return last note from database by client_id."""
    #     self.request_reading_last_note = f'''
    #     SELECT
    #         url_interface, id
    #     FROM
    #         behance_helper
    #     WHERE client_id = '{id}'
    #     ORDER BY id
    #     DESC LIMIT 1
    #     '''
    #     try:
    #         self.cursor.execute(self.request_reading_last_note)
    #         result = self.cursor.fetchall()
    #         self.connection.commit()
    #         return result[0][0].lower()
    #     except Error as error:
    #         print(error)
    #
    #
    # def reading_history(self, id):
    #     """Return info (set urls) from database."""
    #     self.request_reading_history = f'''
    #     SELECT
    #         url_interface, id
    #     FROM
    #         behance_helper
    #     WHERE
    #         client_id='{id}'
    #     '''
    #     try:
    #         self.cursor.execute(self.request_reading_history)
    #         result = self.cursor.fetchall()
    #         self.connection.commit()
    #         result_string = ' '.join(list(set([i[0].lower() for i in result])))
    #         if len(result_string) == 0:
    #             return 'is empty.'
    #         return result_string
    #     except Error as error:
    #         print(error)
    #
    #
