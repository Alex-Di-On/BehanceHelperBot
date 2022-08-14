













                key = bot.message[9:].title()
                try:
                    value = url.get_statistics()[key]
                except KeyError:
                    value = url.statistics[key]
                bot.send_message(f'{key} of {name} is {value}.')





