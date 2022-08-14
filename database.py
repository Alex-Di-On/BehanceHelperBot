import sys
from mysql.connector import connect, Error
from config import configuration


class MetaSingleton(type):
    """Metaclass singleton."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Return _instances[cls]."""
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
    result = None

    def __init__(self):
        """Initialisation of Class Object. Start connection process by default."""
        try:
            self.connection()
        except Error:
            sys.exit('No connection to DataBase.')

    def connection(self) -> None:
        """Connection to database."""
        if self.__connection is None:
            self.__connection = connect(host=self.__host, user=self.__user,
                                        password=self.__password, database=self.__database)
            self.__cursor = self.__connection.cursor()

    def check_connection(self) -> bool:
        """Return status of connection."""
        return self.__connection.is_connected()

    def call_database(self, command: str, id: int, url: str = None) -> None:
        """Calling to database."""
        request = None
        match command:
            case 'insert':
                request = f"INSERT INTO be_helper (client_id, url_interface) VALUES ('{id}', '{url}')"
            case 'last_note':
                request = f"SELECT url_interface, id FROM be_helper WHERE client_id = '{id}' ORDER BY id DESC LIMIT 1"
            case 'history':
                request = f"SELECT url_interface, id FROM be_helper WHERE client_id='{id}'"
        self.__cursor.execute(request)
        self.result = self.__cursor.fetchall()
        self.__connection.commit()

    def get_request_history(self, id: int) -> str:
        """Return request history."""
        self.call_database('history', id)
        return ', '.join(list(set([i[0].lower() for i in self.result])))

    def get_last_note(self, id: int) -> str:
        """Return last note from DataBase by id."""
        self.call_database('last_note', id)
        return self.result[0][0].lower()
