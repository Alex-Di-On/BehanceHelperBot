# from http.server import HTTPServer, BaseHTTPRequestHandler
#
#
# class Server(BaseHTTPRequestHandler):
#
#
#     def do_Get(self):
#         self.send_response(200)
#         self.end_headers()
#
#
# httpserver = HTTPServer(('31.31.196.38', 8000), Server)
# httpserver.serve_forever()
#
# import requests
#
# res = requests.get('http://31.31.196.38:8000/')
# print(res)


# import json
#
# string = '{"update_id":982618780, "message":{"message_id":154,"from":{"id":1172947980,"is_bot":false,"first_name":"Alex","last_name":"Di","username":"Alex_Di_Target","language_code":"ru"},"chat":{"id":1172947980,"first_name":"Alex","last_name":"Di","username":"Alex_Di_Target","type":"private"},"date":1657474460,"text":"\u041f\u0440\u0438\u0432\u0435\u0442!"}}'
#
# print(json.loads(string)['message']['text'])

import requests
from bs4 import BeautifulSoup

user = 'https://www.behance.net/anastazi_li'
URL = 'https://api.behance.net/v2'
METHOD = '/users/anastazi_li'

# res = requests.get(user)
# page = BeautifulSoup(res.text, 'html.parser')
# print(page.find('a', class_='e2e-UserInfo-statValue-followers-count').text)

res = requests.get(URL + METHOD)
print(res.json())
