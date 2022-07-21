from bs4 import BeautifulSoup
import requests


class Parser:
    """Парсер веб-страницы."""

    WEBSITE = 'https://www.behance.net/'
    info_dict = {'Project Views': '0', 'Appreciations': '0', 'Followers': '0', 'Following': '0'}
    place = None

    def __init__(self, user, command):
        self.user = user
        self.command = command

    def get_requests(self):
        """Отправляем запрос на главную страницу автора."""
        return requests.get(self.WEBSITE + self.user)

    def get_html_page(self):
        """Получаем html-страницу для парсинга."""
        return BeautifulSoup(self.get_requests().text, 'html.parser')

    def get_info_dict(self):
        """Generate and return a dictionary with information about the author."""
        try:
            views = self.get_html_page().find('table', class_='UserInfo-userStats-PFk')
            array = [views.find_all('td')[i].text for i in range(len(views.find_all('td')))]
            return {array[a]: array[a + 1] for a in range(len(array))[::2] if a < len(array) - 1}
        except AttributeError:
            return self.info_dict

    def get_behance_info(self):
        """Generate and return the information requested by the client."""
        try:
            if self.command == 'Country':
                return self.get_place()
            return f'{self.command} of {self.user}: {self.get_info_dict()[self.command]}'
        except KeyError:
            return f'{self.command} of {self.user}: 0'

    def get_place(self):
        """Получаем информацию о местонахождении автора."""
        try:
            self.place = self.get_html_page().find('span', class_='e2e-Profile-location').text
            return f'Country of {self.user}: {self.place} {self.get_flag_emoji(self.place)}'
        except AttributeError:
            return f"{self.user} didn't indicate the country on the form."

    def get_flag_emoji(self, country):
        """Getting the emoji flag."""
        country = country.split()
        url = 'https://emojipedia.org/flag-'
        res = BeautifulSoup(requests.get(url + country[-1].lower()).text, 'html.parser').find('title').text
        return res.split()[0]
