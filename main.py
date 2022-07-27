import requests
import time

from behance_helper import BehanceHelper


def get_update_id(data):
    """Return update_id of the Client's last request to the Bot."""
    if not data['result']:
        return 0
    return data['result'][0]['update_id']


def get_update(value=0):
    """Return POST-request for reading info about the Client's last request to the Bot."""
    method = '/getUpdates'
    data = {'offset': value, 'limit': 1, 'timeout': 0}
    return requests.post(BehanceHelper.URL + BehanceHelper.TOKEN + method, data=data)


if __name__ == '__main__':
    id = get_update_id(get_update().json())
    print(f'Start id: {id}')
    while True:
        time.sleep(0.5)
        helper = BehanceHelper(id)
        if helper.get_client_id():
            helper.text_validation()
            id += 1
