import requests
from bs4 import BeautifulSoup
from emoji import emojize


class ParserBehance:
    """Parser of author's web-page on Behance."""

    URL = 'https://www.behance.net/'
    statistics = {'Project Views': 0, 'Appreciations': 0, 'Followers': 0, 'Following': 0}

    def __init__(self, user_name: str):
        """Initialisation of Class Object."""
        self.user_name = user_name

    def get_request(self) -> requests.models.Response:
        """Return GET-request."""
        return requests.get(self.URL + self.user_name)

    def url_validation(self) -> bool:
        """Checking author's registration on Behance."""
        return self.get_request().status_code == 200

    def get_html_page(self) -> object:
        """Return class BeautifulSoup."""
        return BeautifulSoup(self.get_request().text, 'html.parser')

    def get_country(self) -> str:
        """Return country of author from html-page."""
        full_location = self.get_html_page().find('span', class_='e2e-Profile-location').text
        country = full_location.split()[-1]
        match country:
            case 'Federation':
                return 'Russia'
        return country

    def get_flag(self) -> str:
        """Return flag by country."""
        flag = f"{emojize(f':{self.get_country()}:')}"
        if len(flag) > 2:
            return ''
        return flag

    def get_statistics_dict(self) -> dict:
        """Return statistics of author by command from html-page."""
        views = self.get_html_page().find('table', class_='UserInfo-userStats-PFk')
        array = [views.find_all('td')[i].text for i in range(len(views.find_all('td')))]
        return {array[a]: array[a + 1] for a in range(len(array))[::2] if a < len(array) - 1}

    def get_stat(self, message: str) -> str:
        """Return statistics by key."""
        key = message[9:].title()
        try:
            value = self.get_statistics_dict()[key]
        except KeyError:
            value = self.statistics[key]
        return value
