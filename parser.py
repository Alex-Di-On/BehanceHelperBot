from bs4 import BeautifulSoup
import requests


class Parser:
    """Парсер веб-страницы."""

    WEBSITE = 'https://www.behance.net/'

    def __init__(self, user):
        self.user = user

    def get_requests(self):
        """Отправляем запрос на главную страницу автора."""
        return requests.get(self.WEBSITE + self.user)

    def get_html_page(self):
        """Получаем html-страницу для парсинга."""
        return BeautifulSoup(self.get_requests().text, 'html.parser')

    def get_views(self):
        """Получаем информацию о кол-ве просмотров."""
        try:
            views = self.get_html_page().find('td', class_='UserInfo-statColumn-NsR UserInfo-statValue-d3q').text
            return f'Просмотры проекта {self.user}: {views}.'
        except AttributeError:
            return f'Просмотры проекта {self.user}: 0.'

    def get_followers(self):
        """Получаем информацию о кол-ве подписчиков."""
        try:
            followers = self.get_html_page().find('a', class_='e2e-UserInfo-statValue-followers-count').text
            return f'Подписчики {self.user}: {followers}.'
        except AttributeError:
            return f'Подписчики {self.user}: 0.'

    def get_place(self):
        """Получаем информацию о местонахождении автора."""
        try:
            place = self.get_html_page().find('span', class_='e2e-Profile-location').text
            return f'Местонахождение {self.user}: {place}.'
        except AttributeError:
            return f'Не удалось получить информацию.'
