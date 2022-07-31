import requests
import time

from telegram import TelegramAPI


def get_update_id(data):
    """Return update_id of the Client's last request to the Bot."""
    if not data['result']:
        return 0
    return data['result'][0]['update_id']


def get_update(value=0):
    """Return POST-request for reading info about the Client's last request to the Bot."""
    method = '/getUpdates'
    data = {'offset': value, 'limit': 1, 'timeout': 0}
    return requests.post(TelegramAPI.URL + TelegramAPI.TOKEN + method, data=data)


if __name__ == '__main__':
    update_id = get_update_id(get_update().json())
    print(f'Start update_id: {update_id}')
    while True:
        time.sleep(0.5)
        helper = TelegramAPI(update_id)
        # if helper.get_client_id():
        #     helper.text_validation()
        #     update_id += 1
