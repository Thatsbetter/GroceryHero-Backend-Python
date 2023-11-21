import json

import requests

obj = {
    "name": "john 123",
    "password": "123123",
    "email": "123@1234.de",
    "location": "53.68850828741833,9.72187669707107",
    "age": 25,
    "address": "Straße PLZ Stadt "
}

req = requests.post('https://vsis-lehre1.informatik.uni-hamburg.de/api/user/register', json=obj)
res = json.loads(req.text)
print(res)
s = requests.Session()
obj = {
    "password": "123123",
    "email": "123@1234.de",
}

req = s.post('https://vsis-lehre1.informatik.uni-hamburg.de/api/user/login', json=obj)
res = json.loads(req.text)
print(json.dumps(res,indent=3))
req = s.post('https://vsis-lehre1.informatik.uni-hamburg.de/api/shoppingitem/reserve',json={"ids":["56"]})
res = json.loads(req.text)
print(json.dumps(res,indent=3))
req = s.post('https://vsis-lehre1.informatik.uni-hamburg.de/api/shoppingitem/status',json={"id":56,"status":"closed"})
res = json.loads(req.text)
print(json.dumps(res,indent=3))
req = s.post('https://vsis-lehre1.informatik.uni-hamburg.de/api/shoppinglist/nearby')
res = json.loads(req.text)
print(json.dumps(res,indent=3))

