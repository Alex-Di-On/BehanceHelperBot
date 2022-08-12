import sys
import requests
import json
from config import configuration


class TelegramAPI:
    """Class for accessing to Telegram via API."""

    URL = 'https://api.telegram.org/bot'
    TOKEN = configuration['token']
    client_id = None
    message = None

    def __init__(self, identification: int = 0):
        """Initialisation of Class Object."""
        self.identification = identification

    def test_connection(self) -> None:
        """Test connection to Telegram server."""
        method = '/getUpdates'
        data = {'offset': 0, 'limit': 1, 'timeout': 0}
        response = self.get_post_request(method, data)
        if response.status_code != 200:
            sys.exit('Telegram server is not available.')

    def get_post_request(self, method: str, body: dict) -> requests.models.Response:
        """Return POST-request."""
        return requests.post(self.URL + self.TOKEN + method, data=body)

    def get_info(self) -> None:
        """Getting info about Client."""
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        response = self.get_post_request('/getUpdates', data)
        way = response.json()['result'][0]['message']
        self.client_id = way['from']['id']
        self.message = way['text']

    def send_message(self, text: str, command: str = None, button: list = None) -> None:
        """Sending message to Client."""
        data = {'chat_id': self.client_id, 'text': text}
        match command:
            case 'set_buttons':
                data['reply_markup'] = json.dumps({'keyboard': button, 'one_time_keyboard': False})
            case 'del_buttons':
                data['reply_markup'] = json.dumps({'remove_keyboard': True})
        self.get_post_request('/sendMessage', data)
