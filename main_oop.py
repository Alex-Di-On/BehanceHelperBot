import requests  # Библиотека, позволяющая создавать http-запросы.
import time  # Библиотека, позволяющая управлять временем.
import sys


URL = 'https://api.telegram.org/bot'  # Официальный API Telegram для отправки запросов.
TOKEN = '5411737719:AAG7_xCgARflJwofkP-nTiAhcrMIhinltqQ'  # Конфиденциальный токен telegram-бота. Тестовый бот.


class Helper:

    response = None
    response_json = None
    client_id = None

    def __init__(self, identification):
        self.identification = identification

    def get_update(self):
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        self.response = requests.post(URL + TOKEN + method, data=data)

    def convert_response(self):
        if self.response.status_code == 200:
            self.response_json = self.response.json()
        else:
            sys.exit(f'Не удалось получить ответ от Telegram. Код ошибки: {self.response.status_code}.')

    def get_client_id(self):
        if not self.response_json['result']:
            print('Никто не обращался к боту!')
        else:
            self.client_id = self.response_json['result'][0]['message']['from']['id']
            return True


"""Функциональная часть для определения
текущего id с целью запуска основной программы."""


def get_update_id(data):
    """Получаем id, последнего отправленного боту сообщения."""
    if not data['result']:
        return False
    return data['result'][0]['update_id']


def get_update(id):
    """Получаем тело ответа на POST-запрос к боту, по найденному id."""
    method = '/getUpdates'
    data = {'offset': id, 'limit': 1, 'timeout': 0}
    return requests.post(URL + TOKEN + method, data=data)




def get_client_text(data):
    return data['result'][0]['message']['text']


def send_text(id, text):
    action = '/sendMessage'
    body = {'chat_id': id, 'text': text}
    return requests.post(URL + TOKEN + action, data=body)


def text_validation(name, text):
    if text == 'Пасхалка':
        return f'{name}, You won a car!'
    else:
        return f"{name}, I didn't understand you!"


def get_name_client(data):
    return data['result'][0]['message']['from']['first_name']


if __name__ == '__main__':
    id = get_update_id(get_update(0).json())
    print(f'Start id: {id}')
    while True:
        time.sleep(0.5)
        helper = Helper(id)
        helper.get_update()
        helper.convert_response()
        if helper.get_client_id():
            text = get_client_text(helper.response_json)
            name = get_name_client(helper.response_json)
            send_text(helper.client_id, text_validation(name, text))
            id += 1
