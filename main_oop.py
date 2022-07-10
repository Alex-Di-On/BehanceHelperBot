import requests  # Библиотека, позволяющая создавать http-запросы.
import time  # Библиотека, позволяющая управлять временем.


URL = 'https://api.telegram.org/bot'  # Официальный API Telegram для отправки запросов.
TOKEN = '5411737719:AAG7_xCgARflJwofkP-nTiAhcrMIhinltqQ'  # Конфиденциальный токен telegram-бота. Тестовый бот.


class Helper:

    response = None

    def __init__(self, id):
        self.id = id

    def get_update(self):
        method = '/getUpdates'
        data = {'offset': self.id, 'limit': 1, 'timeout': 0}
        self.response = requests.post(URL + TOKEN + method, data=data)

    def get_status(self):
        if self.response.status_code != 200:
            return False
        return True






"""Функциональная часть для определения update_id."""


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



def get_status(code):
    if code != 200:
        return False
    return True


def get_client_id(data):
    if data['result'] == []:
        print('Нет новых сообщений!')
        return False
    return data['result'][0]['message']['from']['id']


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
        if helper.get_status():
            get_update_json = helper.response.json()
            client_id = get_client_id(get_update_json)
            print(client_id)
            if client_id:
                text = get_client_text(get_update_json)
                name = get_name_client(get_update_json)
                send_text(client_id, text_validation(name, text))
                id += 1
