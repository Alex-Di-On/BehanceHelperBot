import requests
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


if __name__ == '__main__':
    update_id = get_update_id(get_update().json())
    print(f'Start update_id: {update_id}')
    while True:
        time.sleep(0.5)
        try:
            bot = TelegramAPI(update_id)
            bot.get_info()
            print(bot.client_id)
            print(bot.message)
            update_id += 1
            print(update_id)
        except IndexError:
            print('Никто не обращался к боту!')





        # time.sleep(0.5)
        #     res = get_update(id)
        #     if get_status(res.status_code):
        #         get_update_json = res.json()
        #         client_id = get_client_id(get_update_json)
        #         print(client_id)
        #         if client_id:
        #             text = get_client_text(get_update_json)
        #             name = get_name_client(get_update_json)
        #             send_text(client_id, text_validation(name, text))
        #             id += 1




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

# def language_test(self, word: str) -> bool:
#     """Return True if message is written in English or False."""
#     for i in list(word):
#         if not ord(i) in range(32, 128):
#             self.send_info(answers['language_test'])
#             return False
#     return True

# def accessing_database(self, command):
#     """Accessing the database to write/read data."""
#     data_base = DataBase(configuration['host'], configuration['user'],
#                          configuration['password'], configuration['database'])
#     data_base.connect()
#     if command == 'insert_client_id_and_url':
#         data_base.insert_data(self.client_id, self.client_message())
#     elif command == 'select_last_note':
#         return data_base.reading_last_note(self.client_id)
#     elif command == 'select_history_client_id':
#         return data_base.reading_history(self.client_id)

# db = DataBase()
# db.connection()
# db.call_database('insert', 6666666, 'Hell')
# db.call_database('last_note', 1172947980)
# print(db.result[0][0].lower())
# db.call_database('history', 1172947980)
# print(' '.join(list(set([i[0].lower() for i in db.result]))))