import requests
import sys
from mysql.connector import Error
import time
import emoji

from database import DataBase
from parser import ParserBehance
from telegram import TelegramAPI
from templates import buttons_menu
from answers import answers


def get_update_id(data: dict) -> int:
    """Return update_id of Client's last request to Bot."""
    if not data['result']:
        return 0
    return data['result'][0]['update_id']


def get_update(value: int = 0) -> requests.models.Response:
    """Return POST-request."""
    method = '/getUpdates'
    data = {'offset': value, 'limit': 1, 'timeout': 0}
    return requests.post(TelegramAPI.URL + TelegramAPI.TOKEN + method, data=data)


def language_test(word: str) -> bool:
    """Checking that message is written in English."""
    for i in list(word):
        if not ord(i) in range(32, 128):
            return False
    return True


if __name__ == '__main__':
    try:
        database = DataBase()
        database.connection()
    except Error:
        sys.exit(answers['quit'])
    update_id = get_update_id(get_update().json())
    print(f'Start update_id: {update_id}')
    while True:
        time.sleep(0.5)
        try:
            bot = TelegramAPI(update_id)
            bot.get_info()
            if database.check_connection():
                if language_test(bot.message):
                    match bot.message:
                        case '/start' | 'CHANGE URL':
                            bot.send_message(answers['start'])
                else:
                    bot.send_message(answers['language_test'])
            else:
                bot.send_message(answers['error_db'])
            update_id += 1
        except IndexError:
            print(answers['nobody_texted'])

# print(emoji.emojize(':Russia:'))

# def text_validation(self) -> None:
#     """Calling the method depending on the message received from the client."""
#     if self.language_test(self.client_message()):
#         if self.client_message() in ['/start', 'CHANGE URL']:
#             self.send_start()
#         elif self.client_message() == 'REQUEST HISTORY':
#             self.get_request_history()
#         elif self.client_message() in self.COMMAND_BOX:
#             user_name = self.accessing_database('select_last_note')
#             info = ParserBehance(user_name, self.client_message())
#             self.send_info(info.get_info())
#         else:
#             self.send_menu()

# def get_request_history(self) -> None:
#     """Sending the result of the database request to Client."""
#     try:
#         self.send_info(f"REQUEST HISTORY: {self.accessing_database('select_history_client_id')}")
#     except:
#         self.send_info(answers['error_db'])


# db = DataBase()
# db.connection()
# db.call_database('insert', 6666666, 'Hell')
# db.call_database('last_note', 1172947980)
# print(db.result[0][0].lower())
# db.call_database('history', 1172947980)
# print(' '.join(list(set([i[0].lower() for i in db.result]))))
