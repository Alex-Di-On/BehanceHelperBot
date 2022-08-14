import requests
from smtplib import SMTP, SMTPAuthenticationError, SMTPConnectError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from emoji import emojize

from database import DataBase
from parser import ParserBehance
from telegram import TelegramAPI
from answers import answers, buttons_menu
from config import configuration


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


def country_filter(region: str) -> str:
    """Changing country for emoji searching."""
    if region.split()[-1] == 'Federation':
        return 'Russia'
    elif region.split()[-1] == 'China':
        return 'China'
    return region


if __name__ == '__main__':
    test = TelegramAPI()
    update_id = test.info_dict['update_id']
    print(f'Start update_id: {update_id}')
    database = DataBase()
    print('Connection to DataBase is successful.')
    while True:
        time.sleep(0.5)
        bot = TelegramAPI(update_id)
        if bot.info_dict['text'] is None:
            print('Nobody texted to Bot.')
            continue
        else:
            if database.check_connection():
                print('DataBase status connection is True.')
                if language_test(bot.info_dict['text']):
                    match bot.info_dict['text']:
                        case '/start' | 'CHANGE URL':
                            bot.send_message(answers['start'], 'del_buttons')
                        case _:
                            bot.send_message('Ведутся технические работы!')
                else:
                    bot.send_message(answers['language_test'])
            else:
                bot.send_message(answers['error_db'])
                print('DataBase status connection is False.')
        update_id += 1
