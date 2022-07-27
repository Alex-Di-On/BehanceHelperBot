from bs4 import BeautifulSoup
import requests


class EmojiFlag:
    """Emoji Flag."""

    URL_EMOJI = 'https://emojipedia.org/flag-'

    def __init__(self, country):
        """Initialisation of Class Object."""
        self.country = country

    def get_flag_emoji(self):
        """Return the emoji flag."""
        location = self.country.split()
        res = BeautifulSoup(requests.get(self.URL_EMOJI + location[-1].lower()).text, 'html.parser').find('title').text
        return res.split()[0]
