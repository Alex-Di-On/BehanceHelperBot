import requests


res = requests.post('http://127.0.0.1:5000/bot', json={"number": "10"})

print(res.json()['result'])
