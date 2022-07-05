import requests  # Библиотека, позволяющая создавать http-запросы.
import time  # Библиотека, позволяющая управлять временем.


URL = 'https://api.telegram.org/bot'  # Официальный API Telegram для отправки запросов.
TOKEN = '5566556459:AAHmi2BQlryt-6UQbBkXPdmw1JizcrGJjdo'  # Конфиденциальный токен telegram-бота.


def get_update_id(data):
    if data['result'] == []:
        return False
    return data['result'][0]['update_id']


def get_update(id):
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
    match text:
        case 'Пасхалка':
            return f'{name}, You won a car!'
        case _:
            return f"{name}, I didn't understand you!"


def get_name_client(data):
    return data['result'][0]['message']['from']['first_name']


if __name__ == '__main__':
    id = get_update_id(get_update(0).json())
    print(f'Start id: {id}')
    while True:
        time.sleep(0.5)
        res = get_update(id)
        if get_status(res.status_code):
            get_update_json = res.json()
            client_id = get_client_id(get_update_json)
            print(client_id)
            if client_id:
                text = get_client_text(get_update_json)
                name = get_name_client(get_update_json)
                send_text(client_id, text_validation(name, text))
                id += 1
