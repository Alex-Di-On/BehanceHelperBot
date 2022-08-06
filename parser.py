import requests
from bs4 import BeautifulSoup


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
        """Setting country of author from html-page."""
        return self.get_html_page().find('span', class_='e2e-Profile-location').text

    def get_statistics(self) -> dict:
        """Return statistics of author by command from html-page."""
        views = self.get_html_page().find('table', class_='UserInfo-userStats-PFk')
        array = [views.find_all('td')[i].text for i in range(len(views.find_all('td')))]
        return {array[a]: array[a + 1] for a in range(len(array))[::2] if a < len(array) - 1}
