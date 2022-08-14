







class MessageHandler:

    def __init__(self, message, ):





    '/start' | 'CHANGE URL':
        bot.send_message(answers['start'], 'del_buttons')

    'REQUEST HISTORY':
        database.call_database('history', bot.client_id)
        history_result = ', '.join(list(set([i[0].lower() for i in database.result])))
        if not history_result:
            bot.send_message(answers['empty_history'])
        else:
            bot.send_message(f"{answers['request_history']} {history_result}.")

    "Author's project views" | "Author's appreciations" |\
         "Author's followers" | "Author's following" | "Author's country":
        try:
            database.call_database('last_note', bot.client_id)
            url = ParserBehance(database.result[0][0].lower())
            name = url.user_name.capitalize()
            if bot.message == "Author's country":
                country = country_filter(url.get_country())
                flag = f"{emojize(f':{country}:')}"
                bot.send_message(f'Country of {name} is {country} {flag}')
            else:
                key = bot.message[9:].title()
                try:
                    value = url.get_statistics()[key]
                except KeyError:
                    value = url.statistics[key]
                bot.send_message(f'{key} of {name} is {value}.')
        except IndexError:
            bot.send_message(answers['no_history'])

        author = ParserBehance(bot.message)
        if author.url_validation():
            database.call_database('insert', bot.client_id, bot.message)
            bot.send_message(answers['menu'], 'set_buttons', buttons_menu)
        else:
            bot.send_message(answers['no_portfolio'])
