import requests


def test_get_token():

    url = 'http://localhost:8422/api/auth'

    payload = {
        'username': 'admin',
        'password': 'admin'
    }

    response = requests.post(url, json=payload)

    print(response.text)
    return response.json().get('access_token')



