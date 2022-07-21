from flask import Flask, request
import requests
import json

application = Flask(__name__)

URL = 'https://api.telegram.org/bot'  # Официальный API Telegram для отправки запросов.
TOKEN = '5566556459:AAHmi2BQlryt-6UQbBkXPdmw1JizcrGJjdo'  # Конфиденциальный токен telegram-бота.

@application.route('/')
def hello():
    return '<p>ПРИВЕТ, Я БОТ</p>'


@application.route('/bot', methods=['GET', 'POST'])
def bot():
    if request.method == 'POST':
        info = json.loads(request.data)
        action = '/sendMessage'
        body = {'chat_id': 1172947980, 'text': info['message']['text']}
        return requests.post(URL + TOKEN + action, data=body)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8443)

