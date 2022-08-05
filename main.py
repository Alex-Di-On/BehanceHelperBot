import requests
import sys
from mysql.connector import Error
import time
from emoji import emojize

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
        if ord(i) not in range(32, 128):
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
        except IndexError:
            print(answers['nobody_texted'])
            continue
        if database.check_connection():
            if language_test(bot.message):
                match bot.message:
                    case '/start' | 'CHANGE URL':
                        bot.send_message(answers['start'], 'del_buttons')
                    case 'REQUEST HISTORY':
                        database.call_database('history', bot.client_id)
                        history_result = ' '.join(list(set([i[0].lower() for i in database.result])))
                        if not history_result:
                            bot.send_message(answers['empty_history'])
                        else:
                            bot.send_message(history_result)
                    case _:
                        try:
                            database.call_database('last_note', bot.client_id)
                            last_note = ParserBehance(database.result[0][0].lower())
                            url_dict_stat = last_note.get_statistics()
                            url_country = last_note.get_country()
                        except IndexError:
                            url_dict_stat = None
                            url_country = answers['no_country']
                        if bot.message == "Author's project views":
                            pass
                        elif bot.message == "Author's appreciations":
                            pass
                        elif bot.message == "Author's followers":
                            pass
                        elif bot.message == "Author's following":
                            pass
                        elif bot.message == "Author's country":
                            bot.send_message(url_country + emojize(f':{url_country}:'))
                        else:
                            author = ParserBehance(bot.message)
                            if author.url_validation():
                                database.call_database('insert', bot.client_id, bot.message)
                                bot.send_message(answers['menu'], 'set_buttons', buttons_menu)
                            else:
                                bot.send_message(answers['no_portfolio'])
            else:
                bot.send_message(answers['language_test'])
        else:
            bot.send_message(answers['error_db'])
        update_id += 1
