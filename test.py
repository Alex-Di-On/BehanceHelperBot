import emoji
import requests

print(emoji.emojize(':Russia:'))


def get_update():
    """Return POST-request to Telegram."""
    method = '/getUpdates'
    data = {'offset': 0, 'limit': 1, 'timeout': 0}
    return requests.post('https://api.telegram.org/bot' + '5560947865:AAFIU9dUBg5pZZ5RatXkUf6nM995TbnPgMU' + method, data=data)


print(type(get_update()))
