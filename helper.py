


# def admin_message(data: dict) -> requests.models.Response:
#     """Sending message to Admin."""
#     method = '/sendMessage'
#     return requests.post(TelegramAPI.URL + TelegramAPI.TOKEN + method, data=data)


def language_test(word: str) -> bool:
    """Checking that message is written in English."""
    for i in list(word):
        if ord(i) not in range(32, 128):
            return False
    return True
