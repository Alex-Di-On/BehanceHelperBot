import requests
import json
from config import configuration


class TelegramAPI:
    """Class for accessing to Telegram via API."""

    URL = 'https://api.telegram.org/bot'
    TOKEN = configuration['token']
    client_id = None

    def __init__(self, identification: int):
        """Initialisation of Class Object."""
        self.identification = identification

    def get_update(self) -> requests.models.Response:
        """Return Response from Telegram."""
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return requests.post(self.URL + self.TOKEN + method, data=data)

    def get_json(self) -> dict:
        """Return Response in json() format."""
        if self.get_update().status_code == 200:
            return self.get_update().json()

    def get_client_id(self) -> int:
        """Return Client id."""
        return self.get_json()['result'][0]['message']['from']['id']

    def get_message(self) -> str:
        """Return text message from Client."""
        return self.get_json()['result'][0]['message']['text']
