import requests
import time
import json
import parser
from config import private_token
from bot_answers import answers


class BehanceHelper:
    """Response processing class from the Telegram API."""

    URL = 'https://api.telegram.org/bot'
    TOKEN = private_token
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
            print(answers['nobody_calling'])
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
        """Call the method depending on the message received from the client."""
        if self.language_test(self.client_message()):
            command_message = ' '.join(self.client_message().split()[:-2])
            if self.client_message() == '/start':
                self.send_start()
            elif command_message in self.COMMAND_BOX:
                user_name = self.client_message().split()[-1]
                object = parser.Parser(user_name, command_message)
                self.send_info(object.get_behance_info())
            else:
                self.send_menu()

    def send_start(self):
        """Приветствуем Клиента."""
        hello = "Please, input author's URL on Behance:"
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': hello}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def send_menu(self):
        """Отправляем Клиенту меню."""
        if self.url_validation():
            hello = 'Please, select the menu item:'
            buttons = {'keyboard': [[f'Project Views of {self.client_message()}'],
                                    [f'Appreciations of {self.client_message()}'],
                                    [f'Followers of {self.client_message()}'],
                                    [f'Following of {self.client_message()}'],
                                    [f'Country of {self.client_message()}']]}
            action = '/sendMessage'
            body = {'chat_id': self.client_id, 'text': hello, 'reply_markup': json.dumps(buttons)}
            return requests.post(self.URL + self.TOKEN + action, data=body)
        else:
            self.send_info('This author has no portfolio on Behance.')

    def send_info(self, text):
        """We send a response to the client."""
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': text}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def url_validation(self):
        """Check that the author is registered on Behance."""
        self.behance_res = requests.get(parser.Parser.WEB_PAGE + self.client_message())
        return self.behance_res.status_code == 200


"""Functional part for the initial launch of the script (trapping Start id)."""


def get_update_id(data):
    """Получаем id, последнего отправленного боту сообщения."""
    if not data['result']:
        return 0
    return data['result'][0]['update_id']


def get_update(id=0):
    """Получаем тело ответа на POST-запрос к боту, по найденному id."""
    method = '/getUpdates'
    data = {'offset': id, 'limit': 1, 'timeout': 0}
    return requests.post(BehanceHelper.URL + BehanceHelper.TOKEN + method, data=data)


if __name__ == '__main__':
    id = get_update_id(get_update().json())
    print(f'Start id: {id}')
    while True:
        time.sleep(0.5)
        helper = BehanceHelper(id)  # Создаем экземпляр родительского класса.
        helper.get_update()  # Получаем ответ на запрос.
        if helper.get_client_id():  # Фиксируем id Клиента.
            helper.text_validation()
            id += 1
