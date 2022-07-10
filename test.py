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

import requests

res = requests.get('http://31.31.196.38:8000/')
print(res)
