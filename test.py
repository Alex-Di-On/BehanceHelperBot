from bs4 import BeautifulSoup
import requests


class Parser:
    """Парсер веб-страницы."""

    WEBSITE = 'https://www.behance.net/'
    info_dict = {'Project Views': '0', 'Appreciations': '0', 'Followers': '0', 'Following': '0'}

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



    # def get_views(self):
    #     """Получаем информацию о кол-ве просмотров."""
    #     try:
    #         views = self.get_html_page().find('table', class_='UserInfo-userStats-PFk')
    #         for cell in views.find_all('td'):
    #             print(cell.text)
    #     except AttributeError:
    #         return f'Просмотры {self.user}: 0.'
    #
    # def get_followers(self):
    #     """Получаем информацию о кол-ве подписчиков."""
    #     try:
    #         followers = self.get_html_page().find('a', class_='e2e-UserInfo-statValue-followers-count').text
    #         return f'Подписчики {self.user}: {followers}.'
    #     except AttributeError:
    #         return f'Подписчики {self.user}: 0.'
    #
    # def get_place(self):
    #     """Получаем информацию о местонахождении автора."""
    #     try:
    #         place = self.get_html_page().find('span', class_='e2e-Profile-location').text
    #         return f'Местонахождение {self.user}: {place}.'
    #     except AttributeError:
    #         return f'Не удалось получить информацию.'


p = Parser('anastazi_li')
print(p.get_info_dict())


p = Parser('rosinadar5')
print(p.get_info_dict())


p = Parser('D3Master')
print(p.get_info_dict())


