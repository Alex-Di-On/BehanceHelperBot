from flask import Flask, request

application = Flask(__name__)


@application.route('/')
def hello():
    return '<p>ПРИВЕТ</p>'


@application.route('/bot', methods=['GET', 'POST'])
def bot():
    if request.method == 'POST':
        print(request.get_json())


if __name__ == '__main__':
    application.run(host='0.0.0.0')
