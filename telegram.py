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

    def get_post_request(self, method: str, body: dict) -> requests.models.Response:
        """Return POST-request."""
        return requests.post(self.URL + self.TOKEN + method, data=body)

    def get_update(self) -> requests.models.Response:
        """Return Response from Telegram."""
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return self.get_post_request('/getUpdates', data)

    def get_client_id(self) -> int:
        """Return Client id."""
        return self.get_update().json()['result'][0]['message']['from']['id']

    def get_message(self) -> str:
        """Return text message from Client."""
        return self.get_update().json()['result'][0]['message']['text']

    def send_message(self, text: str, command: str = None, button: list = None) -> None:
        """Sending message to Client."""
        data = {'chat_id': self.get_client_id(), 'text': text}
        match command:
            case 'set_buttons':
                data['reply_markup'] = json.dumps({'keyboard': button, 'one_time_keyboard': False})
            case 'del_buttons':
                data['reply_markup'] = json.dumps({'remove_keyboard': True})
        self.get_post_request('/sendMessage', data)
