import requests

url = 'http://localhost:8422/api/register'

# params = {
#     'type': 'phone'
# }
#
# payload = {
#     "body": {
#         'username': '173176304221',
#         'password': '1234'
#     }
# }


params = {
    'type': 'email'
}

payload = {
    "body": {
        'username': 'wangyuhuiever@163.com',
        'password': '1234'
    }
}


def register():
    response = requests.post(url, params=params, json=payload)

    print(response.text)


if __name__ == '__main__':
    register()
