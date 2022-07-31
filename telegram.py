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
        action = '/getUpdates'
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        return self.get_post_request(action, data)

    def get_client_id(self) -> int:
        """Return Client id."""
        return self.get_update().json()['result'][0]['message']['from']['id']

    def get_message(self) -> str:
        """Return text message from Client."""
        return self.get_update().json()['result'][0]['message']['text']

    def set_message_data(self, text: str) -> dict:
        """Return data for setting message to Client."""
        return {'chat_id': self.get_client_id(), 'text': text}

    def set_buttons_data(self, button: list, text: str) -> dict:
        """Return data for setting buttons to Client."""
        buttons = {'keyboard': button, 'one_time_keyboard': False}
        return {'chat_id': self.get_client_id(), 'text': text, 'reply_markup': json.dumps(buttons)}

    def del_buttons_data(self, text: str) -> dict:
        """Return data for removing buttons from Client."""
        keyboard_remove = {'remove_keyboard': True}
        return {'chat_id': self.get_client_id(), 'text': text, 'reply_markup': json.dumps(keyboard_remove)}


# a = TelegramAPI(99021817)
# print(a.get_client_id())  # 1172947980
# a.get_post_request('/sendMessage', a.set_buttons_data([['1'], ['2']], 'как дела?'))
# a.get_post_request('/sendMessage', a.del_buttons_data('убрали'))
# a.get_post_request('/sendMessage', a.set_message_data('ffff'))
