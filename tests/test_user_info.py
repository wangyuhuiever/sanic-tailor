import requests
from tests.test_login import get_token

url = 'http://localhost:8422/api/user/info'

headers = {
    'Authorization': f'Bearer {get_token()}'
}

def user_info():
    response = requests.get(url, headers=headers)

    print(response.text)


if __name__ == '__main__':
    user_info()
