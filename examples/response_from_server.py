"""It suppose that there is a server up and running locally"""
import requests

url = 'http://localhost:8080/analyze'
data = {
    'text': 'My name is Alex.',
    'language': 'en'
}

response = requests.post(url, json=data)

print(response.json())