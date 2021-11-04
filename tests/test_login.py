import requests

url = 'http://localhost:8422/api/auth'

params = {
    'type': 'phone'
}

payload = {
    'username': '17317630422',
    'password': '1234'
}


params = {
    'type': 'email'
}

payload = {
    'username': 'wangyuhuiever@163.com',
    'password': '1234'
}


def get_token():
    response = requests.post(url, params=params, json=payload)

    print(response.text)
    return response.json().get('access_token')


if __name__ == '__main__':
    get_token()
