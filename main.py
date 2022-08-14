import requests
from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

from database import DataBase
from parser import ParserBehance
from telegram import TelegramAPI
from answers import answers, buttons_menu


def admin_message(data: dict) -> requests.models.Response:
    """Sending message to Admin."""
    method = '/sendMessage'
    return requests.post(TelegramAPI.URL + TelegramAPI.TOKEN + method, data=data)


def language_test(word: str) -> bool:
    """Checking that message is written in English."""
    for i in list(word):
        if ord(i) not in range(32, 128):
            return False
    return True


if __name__ == '__main__':
    test = TelegramAPI()
    update_id = test.info_dict['update_id']
    print(f'Start update_id: {update_id}')
    database = DataBase()
    print('Connection to DataBase is successful.')
    while True:
        time.sleep(0.5)
        bot = TelegramAPI(update_id)
        message = bot.info_dict['text']
        client_id = bot.info_dict['client_id']
        if message is None:
            print('Nobody texted to Bot.')
            continue
        else:
            if database.check_connection():
                print('DataBase status connection is True.')
                if language_test(message):
                    match message:
                        case '/start' | 'CHANGE URL':
                            bot.send_message(answers['start'], 'del_buttons')
                        case 'REQUEST HISTORY':
                            request_history = database.get_request_history(client_id)
                            if not request_history:
                                bot.send_message(answers['empty_history'])
                            else:
                                bot.send_message(request_history)
                        case "Author's project views" | "Author's appreciations" |\
                             "Author's followers" | "Author's following" | "Author's country":
                            try:
                                url = ParserBehance(database.get_last_note(client_id))
                            except IndexError:
                                bot.send_message(answers['no_history'])
                                update_id += 1
                                continue
                            if message == "Author's country":
                                bot.send_message(url.get_country() + url.get_flag())
                            else:
                                bot.send_message(url.get_stat(message))
                        case _:
                            author = ParserBehance(message)
                            if author.url_validation():
                                database.call_database('insert', client_id, message)
                                bot.send_message(answers['menu'], 'set_buttons', buttons_menu)
                            else:
                                bot.send_message(answers['no_portfolio'])
                else:
                    bot.send_message(answers['language_test'])
            else:
                bot.send_message(answers['error_db'])
                print('DataBase status connection is False.')
        update_id += 1
