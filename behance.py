import requests
import json

from parser import ParserBehance
from config import configuration
from answers import answers
from database import DataBase
from templates import buttons_menu


class BehanceHelper:
    """Response processing class from the Telegram API."""

    URL = 'https://api.telegram.org/bot'
    TOKEN = configuration['token']
    COMMAND_BOX = ['Project Views', 'Appreciations', 'Followers', 'Following', 'Country']
    client_id = None
    behance_res = None

    def __init__(self, identification):
        """Initialisation of Class Object."""
        self.identification = identification

    def get_update(self):
        """Return POST-request to Telegram."""
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return requests.post(self.URL + self.TOKEN + method, data=data)

    def convert_response(self):
        """Return self.get_update().json() if response status is 200."""
        if self.get_update().status_code == 200:
            return self.get_update().json()

    def get_client_id(self):
        """Getting client_id or output the result of the query to the console. Return True or False."""
        try:
            self.client_id = self.convert_response()['result'][0]['message']['from']['id']
            return True
        except:
            print(answers['nobody_calling'] + str(self.get_update().status_code))
            return False

    def client_message(self):
        """Return text message from Client."""
        return self.convert_response()['result'][0]['message']['text']

    def text_validation(self):
        """Calling the method depending on the message received from the client."""
        if self.language_test(self.client_message()):
            command_message = ' '.join(self.client_message().split()[:-2])
            if self.client_message() in ['/start', 'CHANGE URL']:
                self.send_start()
            elif self.client_message() == 'REQUEST HISTORY':
                self.get_request_history()
            elif command_message in self.COMMAND_BOX:
                user_name = self.client_message().split()[-1]
                info = ParserBehance(user_name, command_message)
                self.send_info(info.get_info())
            else:
                self.send_menu()

    def send_start(self):
        """Sending a message to the Client for /start."""
        keyboard_remove = {'remove_keyboard': True}
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': answers['/start'], 'reply_markup': json.dumps(keyboard_remove)}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def get_request_history(self):
        """Sending the result of the database request to Client."""
        try:
            self.send_info(f"REQUEST HISTORY: {self.accessing_database('select_history_client_id')}")
        except:
            self.send_info(answers['error_db'])

    def send_info(self, text):
        """Sending info_response to the Client."""
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': text}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def send_menu(self):
        """Sending menu to the Client if self.url_validation is True."""
        if self.url_validation():
            self.accessing_database('insert_client_id_and_url')
            # templates = ['Project Views of ', 'Appreciations of ', 'Followers of ', 'Following of ', 'Country of ']
            # buttons_list = [[i + self.client_message()] for i in templates] + [['REQUEST HISTORY'], ['CHANGE URL']]
            buttons = {'keyboard': buttons_menu, 'one_time_keyboard': False}
            action = '/sendMessage'
            body = {'chat_id': self.client_id, 'text': answers['menu'], 'reply_markup': json.dumps(buttons)}
            return requests.post(self.URL + self.TOKEN + action, data=body)
        else:
            self.send_info(answers['no_portfolio'])

    def url_validation(self):
        """Return True or False if author is registered on Behance."""
        self.behance_res = requests.get(ParserBehance.WEB_PAGE + self.client_message())
        return self.behance_res.status_code == 200

    def accessing_database(self, command):
        """Accessing the database to write/read data."""
        data_base = DataBase(configuration['host'], configuration['user'],
                             configuration['password'], configuration['database'],)
        data_base.connect()
        if command == 'insert_client_id_and_url':
            data_base.insert_data(self.client_id, self.client_message())
        elif command == 'select_last_note':
            return data_base.reading_last_note(self.client_id)
        elif command == 'select_history_client_id':
            return data_base.reading_history(self.client_id)

    def language_test(self, word):
        """Return True if message is written in English or False."""
        for i in list(word):
            if not ord(i) in range(32, 128):
                self.send_info(answers['language_test'])
                return False
        return True
