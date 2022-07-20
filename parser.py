from bs4 import BeautifulSoup
import requests


class Parser:
    """Парсер веб-страницы."""

    WEBSITE = 'https://www.behance.net/'
    info_dict = {'Views': '0', 'Appreciations': '0', 'Followers': '0', 'Following': '0'}
    place = None

    def __init__(self, user):
        self.user = user

    def get_requests(self):
        """Отправляем запрос на главную страницу автора."""
        return requests.get(self.WEBSITE + self.user)

    def get_html_page(self):
        """Получаем html-страницу для парсинга."""
        return BeautifulSoup(self.get_requests().text, 'html.parser')

    def get_info_dict(self):
        """Получаем словарь: описание - значение."""
        try:
            views = self.get_html_page().find('table', class_='UserInfo-userStats-PFk')
            keys = []
            values = []
            for cell in range(len(views.find_all('td'))):
                if cell % 2 == 0:
                    keys.append(views.find_all('td')[cell].text)
                else:
                    values.append(views.find_all('td')[cell].text)
            return dict(zip(keys, values))
        except AttributeError:
            return self.info_dict

    def get_views(self):
        """Получаем информацию о кол-ве просмотров."""
        try:
            return f'Views of {self.user}: {self.get_info_dict()["Project Views"]}'
        except KeyError:
            return f'Views of {self.user}: 0'

    def get_appreciations(self):
        """Получаем информацию о кол-ве оценок."""
        try:
            return f'Appreciations of {self.user}: {self.get_info_dict()["Appreciations"]}'
        except KeyError:
            return f'Appreciations of {self.user}: 0'

    def get_followers(self):
        """Получаем информацию о кол-ве подписчиков."""
        try:
            return f'Followers of {self.user}: {self.get_info_dict()["Followers"]}'
        except KeyError:
            return f'Followers of {self.user}: 0'

    def get_following(self):
        """Получаем информацию о кол-ве подписок."""
        try:
            return f'Following of {self.user}: {self.get_info_dict()["Following"]}'
        except KeyError:
            return f'Following of {self.user}: 0'

    def get_place(self):
        """Получаем информацию о местонахождении автора."""
        try:
            self.place = self.get_html_page().find('span', class_='e2e-Profile-location').text
            return f'Country of {self.user}: {self.place} {self.get_flag_emoji(self.place)}'
        except AttributeError:
            return f"{self.user} didn't indicate the country on the form."

    def get_flag_emoji(self, country):
        country = country.split()
        url = 'https://emojipedia.org/flag-'
        res = BeautifulSoup(requests.get(url + country[-1].lower()).text, 'html.parser').find('title').text
        return res.split()[0]
