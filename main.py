from telegram import TelegramAPI
from database import DataBase
from parser import ParserBehance
from helper_box import admin_email, bot_answers, buttons_menu, language_test
from smtplib import SMTPAuthenticationError, SMTPConnectError
import time

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
                            bot.send_message(bot_answers['start'], 'del_buttons')
                        case 'REQUEST HISTORY':
                            request_history = database.get_request_history(client_id)
                            if not request_history:
                                bot.send_message(bot_answers['empty_history'])
                            else:
                                bot.send_message(request_history)
                        case "Author's project views" | "Author's appreciations" |\
                             "Author's followers" | "Author's following" | "Author's country":
                            try:
                                url = ParserBehance(database.get_last_note(client_id))
                            except IndexError:
                                bot.send_message(bot_answers['no_history'])
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
                                bot.send_message(bot_answers['menu'], 'set_buttons', buttons_menu)
                            else:
                                bot.send_message(bot_answers['no_portfolio'])
                else:
                    bot.send_message(bot_answers['language_test'])
            else:
                bot.send_message(bot_answers['error_db'])
                print('DataBase status connection is False.')
                try:
                    admin_email()
                except SMTPAuthenticationError:
                    bot.send_message('DataBaseError. SMTPAuthenticationError.', 'admin')
                except SMTPConnectError:
                    bot.send_message('DataBaseError. SMTPConnectError.', 'admin')
        update_id += 1
