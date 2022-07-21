from bs4 import BeautifulSoup
import requests


class Parser:
    """Parser of the author's web page on Behance."""

    WEB_PAGE = 'https://www.behance.net/'
    URL_EMOJI = 'https://emojipedia.org/flag-'
    INFO_DICT = {'Project Views': '0', 'Appreciations': '0', 'Followers': '0', 'Following': '0'}
    country = None

    def __init__(self, user_name, command_message):
        """Initialisation of Class Object."""
        self.user_name = user_name
        self.command_message = command_message

    def get_requests(self):
        """Send a request to the author's WEB_PAGE."""
        return requests.get(self.WEB_PAGE + self.user_name)

    def get_html_page(self):
        """We get the html-page for parsing."""
        return BeautifulSoup(self.get_requests().text, 'html.parser')

    def get_info_dict(self):
        """Generate and return a dictionary with information about the author."""
        try:
            views = self.get_html_page().find('table', class_='UserInfo-userStats-PFk')
            array = [views.find_all('td')[i].text for i in range(len(views.find_all('td')))]
            return {array[a]: array[a + 1] for a in range(len(array))[::2] if a < len(array) - 1}
        except AttributeError:
            return self.INFO_DICT

    def get_behance_info(self):
        """Generate and return the information from WEB_PAGE."""
        try:
            if self.command_message == 'Country':
                return self.get_country()
            return f'{self.command_message} of {self.user_name}: {self.get_info_dict()[self.command_message]}'
        except KeyError:
            return f'{self.command_message} of {self.user_name}: 0'

    def get_country(self):
        """Return information of author's location."""
        try:
            self.country = self.get_html_page().find('span', class_='e2e-Profile-location').text
            return f'Country of {self.user_name}: {self.country} {self.get_flag_emoji(self.country)}'
        except AttributeError:
            return f"{self.user_name} didn't indicate the country on the form."

    def get_flag_emoji(self, place):
        """Getting the emoji flag."""
        place = place.split()
        res = BeautifulSoup(requests.get(self.URL_EMOJI + place[-1].lower()).text, 'html.parser').find('title').text
        return res.split()[0]
