from mysql.connector import connect
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
    result = None

    def connection(self) -> None:
        """Connection to database."""
        if self.__connection is None:
            self.__connection = connect(host=self.__host, user=self.__user,
                                        password=self.__password, database=self.__database)
            self.__cursor = self.__connection.cursor()

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
