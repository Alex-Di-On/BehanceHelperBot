import requests
import time
import sys
import json
import parser


class BehanceHelper:
    """Базовый класс обработки ответа от API Telegram."""

    URL = 'https://api.telegram.org/bot'
    TOKEN = '5560947865:AAFIU9dUBg5pZZ5RatXkUf6nM995TbnPgMU'
    COMMAND_BOX = ['Views', 'Appreciations', 'Followers', 'Following', 'Country']
    client_id = None
    behance_res = None

    def __init__(self, identification):
        self.identification = identification

    def get_update(self):
        """Получаем результат POST-запроса к Telegram."""
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return requests.post(self.URL + self.TOKEN + method, data=data)

    def convert_response(self):
        """Конвертируем ответ в json(), если статус ответа - 200."""
        if self.get_update().status_code == 200:
            return self.get_update().json()
        return sys.exit(f'Не удалось получить ответ от Telegram. Код ошибки: {self.get_update().status_code}.')

    def get_client_id(self):
        """Получаем client_id или выводим в консоль результат запроса."""
        if not self.convert_response()['result']:
            print('Никто не обращался к боту!')
        else:
            self.client_id = self.convert_response()['result'][0]['message']['from']['id']
            return True

    def client_message(self):
        """Получаем текст сообщения от Клиента."""
        return self.convert_response()['result'][0]['message']['text']

    def language_test(self, word):
        """Check that the message is written in English."""
        for i in list(word):
            if not ord(i) in range(32, 128):
                self.send_info("I don't understand you. Use English, please.")
                return False
        return True

    def text_validation(self):
        """Call the method depending on the message received from the client."""
        message = self.client_message().split()[0]
        if self.language_test(message):
            if message == '/start':
                self.send_start()
            elif message in self.COMMAND_BOX:
                user_name = self.client_message().split()[2]
                object = parser.Parser(user_name)
                match message:
                    case 'Views':
                        self.send_info(object.get_views())
                    case 'Appreciations':
                        self.send_info(object.get_appreciations())
                    case 'Followers':
                        self.send_info(object.get_followers())
                    case 'Following':
                        self.send_info(object.get_following())
                    case 'Country':
                        self.send_info(object.get_place())
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
            buttons = {'keyboard': [[f'Views of {self.client_message()}'],
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
        self.behance_res = requests.get(parser.Parser.WEBSITE + self.client_message())
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
