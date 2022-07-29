import requests
from bs4 import BeautifulSoup

from answers import answers
from database import DataBase
import database
from config import configuration


class ParserBehance:
    """Parser of the author's web page on Behance."""

    WEB_PAGE = 'https://www.behance.net/'
    INFO_DICT = {'Project Views': '0', 'Appreciations': '0', 'Followers': '0', 'Following': '0'}
    country = None

    def __init__(self, user_name, command_message):
        """Initialisation of Class Object."""
        self.user_name = user_name
        self.command_message = command_message

    def get_requests(self):
        """Return request to the author's WEB_PAGE."""
        return requests.get(self.WEB_PAGE + self.user_name)

    def get_html_page(self):
        """Return html-page for parsing."""
        return BeautifulSoup(self.get_requests().text, 'html.parser')

    def get_stat_dict(self):
        """Generate and return dict with information about the author
        or return INFO_DICT if author hasn't portfolio statistics."""
        try:
            views = self.get_html_page().find('table', class_='UserInfo-userStats-PFk')
            array = [views.find_all('td')[i].text for i in range(len(views.find_all('td')))]
            return {array[a]: array[a + 1] for a in range(len(array))[::2] if a < len(array) - 1}
        except AttributeError:
            return self.INFO_DICT

    def get_country(self):
        """Return self.country."""
        self.country = self.get_html_page().find('span', class_='e2e-Profile-location').text
        if self.country.split()[-1] == 'Federation':
            self.country = 'Russia'
        elif self.country.split()[-1] == 'China':
            self.country = 'China'
        return self.country

    def country_validation(self):
        """Checking if the country listed by the author is in our database."""
        data_base = DataBase(configuration['host'], configuration['user'],
                             configuration['password'], configuration['database'])
        data_base.connect()
        if self.get_country() in data_base.reading_all_countries():
            return True
        return False

    def return_flag(self):
        """Return emoji_flag"""
        data_base = DataBase(configuration['host'], configuration['user'],
                             configuration['password'], configuration['database'])
        data_base.connect()
        return data_base.reading_emoji_flag(self.get_country())

    def get_location_info(self):
        """Return information (string) of author's location. """
        try:
            if self.country_validation():
                return f'Country of {self.user_name}: {self.country} {self.return_flag()}'
            return f'Country of {self.user_name}: {self.country}'
        except AttributeError:
            return self.user_name + answers['no_country']

    def get_info(self):
        """Return information (string) using command_message to dict with information about author statistics or
        if there is no key in dict return information (string) with zero value. For Country use special method."""
        try:
            if self.command_message == 'Country':
                return self.get_location_info()
            return f'{self.command_message} of {self.user_name}: {self.get_stat_dict()[self.command_message]}'
        except KeyError:
            return f'{self.command_message} of {self.user_name}: 0'

