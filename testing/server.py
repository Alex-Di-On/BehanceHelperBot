from flask import Flask, request


application = Flask(__name__)


@application.route('/')
def hello_world():
    return '<p>ПРИВЕТ</p>'


@application.route('/admin')
def hello_world_1():
    return '<p>ПРИВЕТ, Я АДМИН</p>'


@application.route('/bot', methods=['GET', 'POST'])
def hello_world_2():
    if request.method == 'POST':
        return {'result': int(request.get_json()['number']) ** 2}


if __name__ == '__main__':
    application.run()
