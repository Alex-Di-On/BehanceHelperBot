import requests
import time
import json
import parser
from config import configuration
from bot_answers import answers
from behance_helper_bd import DataBaseAction


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
        """Getting the result of a POST request to Telegram."""
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return requests.post(self.URL + self.TOKEN + method, data=data)

    def convert_response(self):
        """Converting response to json() if response status is 200."""
        if self.get_update().status_code == 200:
            return self.get_update().json()

    def get_client_id(self):
        """Getting client_id or output the result of the query to the console."""
        try:
            self.client_id = self.convert_response()['result'][0]['message']['from']['id']
            return True
        except:
            print(answers['nobody_calling'] + str(self.get_update().status_code))
            return False

    def client_message(self):
        """Receiving a text message from Client."""
        return self.convert_response()['result'][0]['message']['text']

    def language_test(self, word):
        """Check that the message is written in English."""
        for i in list(word):
            if not ord(i) in range(32, 128):
                self.send_info(answers['language_test'])
                return False
        return True

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
                object = parser.Parser(user_name, command_message)
                self.send_info(object.get_behance_info())
            else:
                self.send_menu()

    def send_start(self):
        """Sending a message to the Client for /start."""
        keyboard_remove = {'remove_keyboard': True}
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': answers['/start'], 'reply_markup': json.dumps(keyboard_remove)}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def send_menu(self):
        """Sending menu to the Client."""
        if self.url_validation():
            self.accessing_database('insert_client_id_and_url')
            buttons = {'keyboard': [[f'Project Views of {self.client_message()}'],
                                    [f'Appreciations of {self.client_message()}'],
                                    [f'Followers of {self.client_message()}'],
                                    [f'Following of {self.client_message()}'],
                                    [f'Country of {self.client_message()}'],
                                    ['REQUEST HISTORY'],
                                    ['CHANGE URL']],
                       'one_time_keyboard': False}
            action = '/sendMessage'
            body = {'chat_id': self.client_id, 'text': answers['menu'], 'reply_markup': json.dumps(buttons)}
            return requests.post(self.URL + self.TOKEN + action, data=body)
        else:
            self.send_info(answers['no_portfolio'])

    def send_info(self, text):
        """Sending a info_response to the Client."""
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': text}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def url_validation(self):
        """Checking that the author is registered on Behance."""
        self.behance_res = requests.get(parser.Parser.WEB_PAGE + self.client_message())
        return self.behance_res.status_code == 200

    def accessing_database(self, command):
        """Accessing the database to write/read data."""
        data_base = DataBaseAction('31.31.196.38', 'u1726449_alex', 'eY4vT5pM6m', 'u1726449_default',
                                   self.client_id, self.client_message())
        data_base.connect()
        if command == 'insert_client_id_and_url':
            data_base.insert_data()
        elif command == 'select_client_id':
            return data_base.reading_data()

    def get_request_history(self):
        """Sending the result of the database request to Client."""
        try:
            self.send_info(f"REQUEST HISTORY: {self.accessing_database('select_client_id')}")
        except:
            self.send_info(answers['error_db'])


"""Functional part for the initial launch of the script (trapping Start id)."""


def get_update_id(data):
    """Getting id of the last message sent to the bot."""
    if not data['result']:
        return 0
    return data['result'][0]['update_id']


def get_update(id=0):
    """Getting the response body of the POST request to the bot, by the id found."""
    method = '/getUpdates'
    data = {'offset': id, 'limit': 1, 'timeout': 0}
    return requests.post(BehanceHelper.URL + BehanceHelper.TOKEN + method, data=data)


if __name__ == '__main__':
    id = get_update_id(get_update().json())
    print(f'Start id: {id}')
    while True:
        time.sleep(0.5)
        helper = BehanceHelper(id)
        if helper.get_client_id():
            helper.text_validation()
            id += 1
