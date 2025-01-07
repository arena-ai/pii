"""It suppose that the service is up and running on port 8080"""
import requests
import os

def test_service():
    hostname = os.environ.get('SERVICE_HOSTNAME', 'localhost')
    url = f"http://{hostname}:8080/analyze"
    data = {
        'text': 'My name is Alex.',
        'language': 'en'
    }
    print(f"Testing service at: {url}")
    response = requests.post(url, json=data)
    res = response.json()
    assert len(res)==1
