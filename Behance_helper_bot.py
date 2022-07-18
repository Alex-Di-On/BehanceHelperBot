import requests
import time
import sys
from bs4 import BeautifulSoup

URL = 'https://api.telegram.org/bot'
TOKEN = '5560947865:AAFIU9dUBg5pZZ5RatXkUf6nM995TbnPgMU'


class BehanceHelper:
    """Базовый класс обработки ответа от API Telegram."""

    client_id = None

    def __init__(self, identification):
        self.identification = identification

    def get_update(self):
        """Получаем результат POST-запроса к Telegram."""
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return requests.post(URL + TOKEN + method, data=data)

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

    def text_filtration(self):
        """Фильтруем запрос Клиента."""
        hello = 'Введите URL автора на Behance, чтобы узнать его кол-во подписчиков! Например, anastazi_li'
        if self.client_message() == '/start':
            action = '/sendMessage'
            body = {'chat_id': self.client_id, 'text': hello}
            return requests.post(URL + TOKEN + action, data=body)
        return self.client_message()


class FollowersCounter(BehanceHelper):
    """Дочерний класс который отправляет Клиенту информационное сообщение."""

    behance_res = None
    followers = None
    info_message = 'Не удалось найти пользователя.'

    def url_validation(self):
        """Проверяем, существует ли такой пользователь."""
        user = f'https://www.behance.net/{self.text_filtration()}'
        self.behance_res = requests.get(user)
        if self.behance_res.status_code == 200:
            return True

    def get_followers_count(self):
        """Получаем кол-во подписчиков."""
        if self.url_validation():
            page = BeautifulSoup(self.behance_res.text, 'html.parser')
            self.followers = page.find('a', class_='e2e-UserInfo-statValue-followers-count').text
            self.info_message = f'Кол-во подписчиков: {self.followers}'

    def send_info_message(self):
        """Отправляем ответ Клиенту."""
        action = '/sendMessage'
        body = {'chat_id': self.client_id, 'text': self.info_message}
        return requests.post(URL + TOKEN + action, data=body)


"""Функциональная часть"""


def get_update_id(data):
    """Получаем id, последнего отправленного боту сообщения."""
    if not data['result']:
        return False
    return data['result'][0]['update_id']


def get_update(id=0):
    """Получаем тело ответа на POST-запрос к боту, по найденному id."""
    method = '/getUpdates'
    data = {'offset': id, 'limit': 1, 'timeout': 0}
    return requests.post(URL + TOKEN + method, data=data)


if __name__ == '__main__':
    id = get_update_id(get_update().json())
    print(f'Start id: {id}')

    while True:
        time.sleep(0.3)
        helper = FollowersCounter(id)  # Создаем экземпляр класса.
        helper.get_update()  # Получаем ответ на запрос.
        if helper.get_client_id():  # Возвращает True, если кто-то обратился и фиксирует id Пользователя.
            helper.text_filtration()  # Фильтруем команду Клиенту.
            helper.get_followers_count()  # Получаем кол-во подписчиков.
            helper.send_info_message()  # Отправляем ответ Пользователю.
            id += 1  # Увеличиваем id для обработки нового входящего сообщения от Пользователя.