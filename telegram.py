import sys
import requests
import json
from requests import Response, HTTPError
from config import configuration


class TelegramAPI:
    """Class for accessing to Telegram via API."""

    __URL = 'https://api.telegram.org/bot'
    __TOKEN = configuration['token']
    client_id = None
    message = None

    def __init__(self, identification: int = 0):
        """Initialisation of Class Object."""
        self.identification = identification
        print(self.check_status_code())
        self.info_dict = self.get_info_dict()

    def get_post_request(self, method: str, body: dict) -> requests.models.Response:
        """Return POST-request."""
        return requests.post(self.__URL + self.__TOKEN + method, data=body)

    def get_response(self, method: str = '/getUpdates', data=None) -> Response:
        """Return Response."""
        if data is None:
            data = {'offset': 0, 'limit': 1, 'timeout': 0}
        return self.get_post_request(method, data)

    def check_status_code(self) -> str:
        """Return warning message to console."""
        if self.get_response().status_code != 200:
            return 'Telegram server is offline. Please, wait!'
        return 'Telegram server is online.'

    def get_info_dict(self) -> dict:
        """Return info_dict."""
        info_dict = {'update_id': 0, 'client_id': 0, 'text': None}
        try:
            data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
            res_dict = self.get_response(data=data).json()
            if not res_dict['result']:
                return info_dict
            info_dict['update_id'] = res_dict['result'][0]['update_id']
            way = res_dict['result'][0]['message']
            info_dict['client_id'] = way['from']['id']
            info_dict['text'] = way['text']
            return info_dict
        except HTTPError:
            return info_dict

    def get_info(self) -> None:
        """Getting info about Client."""
        data = {'offset': self.identification, 'limit': 1, 'timeout': 0}
        response = self.get_post_request('/getUpdates', data)
        way = response.json()['result'][0]['message']
        self.client_id = way['from']['id']
        self.message = way['text']

    def send_message(self, text: str, command: str = None, button: list = None) -> None:
        """Sending message to Client."""
        data = {'chat_id': self.info_dict['client_id'], 'text': text}
        match command:
            case 'set_buttons':
                data['reply_markup'] = json.dumps({'keyboard': button, 'one_time_keyboard': False})
            case 'del_buttons':
                data['reply_markup'] = json.dumps({'remove_keyboard': True})
        self.get_post_request('/sendMessage', data)
