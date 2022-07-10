import requests  # Библиотека, позволяющая создавать http-запросы.
import time  # Библиотека, позволяющая управлять временем.
import sys  # Библиотека, позволяющая остановить выполнение программы.


class Helper:
    """Класс-помощник, который обрабатывает результат запроса к Telegram."""

    URL = 'https://api.telegram.org/bot'  # Официальный API Telegram для отправки запросов.
    TOKEN = '5411737719:AAG7_xCgARflJwofkP-nTiAhcrMIhinltqQ'  # Конфиденциальный токен telegram-бота. Тестовый бот.
    response = None
    response_json = None
    client_id = None
    client_name = None
    client_text = None
    ANSWERS = {0: 'Я тебя не понимаю!',
               1: 'Ты выиграл машину!',
               2: 'Когда напишешь код?'}

    def __init__(self, identification):
        self.identification = identification

    def get_update(self):
        """Получаем результат POST-запроса к Telegram."""
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        self.response = requests.post(self.URL + self.TOKEN + method, data=data)

    def convert_response(self):
        """Конвертируем ответ в json(), если статус ответа - 200."""
        if self.response.status_code == 200:
            self.response_json = self.response.json()
        else:
            sys.exit(f'Не удалось получить ответ от Telegram. Код ошибки: {self.response.status_code}.')

    def get_client_id(self):
        """Получаем client_id или выводим в консоль результат запроса."""
        if not self.response_json['result']:
            print('Никто не обращался к боту!')
        else:
            self.client_id = self.response_json['result'][0]['message']['from']['id']
            return True

    def client_information(self):
        """Фиксируем Имя Пользователя и Текст сообщения."""
        self.client_name = self.response_json['result'][0]['message']['from']['first_name']
        self.client_text = self.response_json['result'][0]['message']['text']

    def text_validation(self):
        """Валидируем текст сообщения и возвращаем ключ ответа."""
        if self.client_text == 'Пасхалка':
            return 1
        elif self.client_text == 'Виктор':
            return 2
        return 0

    def send_message(self):
        """Отправляем ответ Пользователю."""
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': self.ANSWERS[self.text_validation()]}
        return requests.post(self.URL + self.TOKEN + action, data=body)


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
    return requests.post(Helper.URL + Helper.TOKEN + method, data=data)


if __name__ == '__main__':
    id = get_update_id(get_update(0).json())
    print(f'Start id: {id}')
    while True:
        time.sleep(0.5)
        helper = Helper(id)  # Создаем экземпляр класса.
        helper.get_update()  # Получаем ответ на запрос.
        helper.convert_response()  # Если ответ 200, конвертируем его в json(), если нет - останавливаем программу.
        if helper.get_client_id():  # Возвращает True, если кто-то обратился и фиксирует id Пользователя.
            helper.client_information()  # Фиксируем Имя Пользователя и Текст сообщения.
            helper.send_message()  # Отправляем ответ Пользователю.
            id += 1  # Увеличиваем id для обработки нового входящего сообщения от Пользователя.
