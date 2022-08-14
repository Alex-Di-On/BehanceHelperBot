













    # "Author's project views" | "Author's appreciations" |\
    #      "Author's followers" | "Author's following" | "Author's country":
    #     try:
    #         database.call_database('last_note', bot.client_id)
    #         url = ParserBehance(database.result[0][0].lower())
    #         name = url.user_name.capitalize()
    #         if bot.message == "Author's country":
    #             country = country_filter(url.get_country())
    #             flag = f"{emojize(f':{country}:')}"
    #             bot.send_message(f'Country of {name} is {country} {flag}')
    #         else:
    #             key = bot.message[9:].title()
    #             try:
    #                 value = url.get_statistics()[key]
    #             except KeyError:
    #                 value = url.statistics[key]
    #             bot.send_message(f'{key} of {name} is {value}.')
    #     except IndexError:
    #         bot.send_message(answers['no_history'])




