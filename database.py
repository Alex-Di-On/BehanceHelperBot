from mysql.connector import connect, Error
from config import configuration
# class Singleton(object):
#
#     __instance = None
#
#     def __init__(self, cls):
#         self._cls = cls
#
#     def instance(self):
#         if self.__instance is None:
#             self.__instance = self._cls()
#             return self.__instance
#         return self.__instance
#
#     def __call__(self):
#         raise TypeError('Singletons must be accessed through `instance()`.')
#
#     def __instancecheck__(self, inst):
#         return isinstance(inst, self._cls)
#
# @Singleton

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
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

    def connect(self):
        """Connection to the database."""
        if self.__connection is None:
            try:
                self.__connection = connect(host=self.__host,
                                            user=self.__user,
                                            password=self.__password,
                                            database=self.__database)
                self.__cursor = self.__connection.cursor()
                print('Подключились')
                return self.__cursor
            except Error as error:
                print(error)

    def save(self):
        self.__connection.commit()


class User:
    request = None

    def __init__(self, cursor, id, url):
        self.cursor = cursor
        self.id = id
        self.url = url

    # request_reading_last_note = None
    # request_reading_history = None
    # request_emoji_flag = None
    # request_all_countries = None


    def query(self, command):
        match command:
            case 'insert':
                self.request = self.insert_data()
        try:
            self.cursor.execute(self.request)
            db1.save()
        except Error as error:
            print(error)



    def insert_data(self):
        """Insert data into database."""
        return f'''
        INSERT INTO behance_helper (
            client_id,
            url_interface)
        VALUES ('{self.id}', '{self.url}')
        '''





db1 = DataBase()
user = User(db1.connect(), 88695050, 'VICTOR')
user.query('insert')



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
    # def reading_all_countries(self):
    #     """Return array of all countries from database."""
    #     self.request_all_countries = f'''
    #     SELECT
    #         country, id
    #     FROM
    #         emoji_flags
    #     '''
    #     try:
    #         self.cursor.execute(self.request_all_countries)
    #         result = self.cursor.fetchall()
    #         self.connection.commit()
    #         countries = [i[0] for i in result]
    #         return countries
    #     except Error as error:
    #         print(error)
    #
    #
    # def reading_emoji_flag(self, location):
    #     """Return emoji flag from database by location."""
    #     self.request_emoji_flag = f'''
    #     SELECT
    #         flag, id
    #     FROM
    #         emoji_flags
    #     WHERE country = '{location}'
    #     '''
    #     try:
    #         self.cursor.execute(self.request_emoji_flag)
    #         result = self.cursor.fetchall()
    #         self.connection.commit()
    #         return result[0][0].lower()
    #     except Error as error:
    #         print(error)