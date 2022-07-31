import requests
import json
from config import configuration


class TelegramAPI:
    """Class for accessing to Telegram via API."""

    URL = 'https://api.telegram.org/bot'
    TOKEN = configuration['token']

    def __init__(self, identification: int):
        """Initialisation of Class Object."""
        self.identification = identification

    def get_update(self) -> requests.models.Response:
        """Return Response from Telegram."""
        method = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return requests.post(self.URL + self.TOKEN + method, data=data)

    def get_client_id(self) -> int:
        """Return Client id."""
        return self.get_update().json()['result'][0]['message']['from']['id']

    def get_message(self) -> str:
        """Return text message from Client."""
        return self.get_update().json()['result'][0]['message']['text']

    def send_message(self, text: str) -> requests.models.Response:
        """Sending message to Client."""
        action = '/sendMessage'
        body = {'chat_id': self.get_client_id(), 'text': text}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def send_buttons(self, button: list, text: str) -> requests.models.Response:
        """Sending buttons with message to Client."""
        buttons = {'keyboard': button, 'one_time_keyboard': False}
        action = '/sendMessage'
        body = {'chat_id': self.get_client_id(), 'text': text, 'reply_markup': json.dumps(buttons)}
        return requests.post(self.URL + self.TOKEN + action, data=body)

    def del_buttons(self, text: str) -> requests.models.Response:
        """Removing buttons from Client."""
        keyboard_remove = {'remove_keyboard': True}
        action = '/sendMessage'
        body = {'chat_id': self.get_client_id(), 'text': text, 'reply_markup': json.dumps(keyboard_remove)}
        return requests.post(self.URL + self.TOKEN + action, data=body)
