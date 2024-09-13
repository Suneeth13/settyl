import requests

url = 'http://127.0.0.1:5000/negotiate'
data = {'message': 'I offer $60'}

response = requests.post(url, json=data)
print(response.json())
