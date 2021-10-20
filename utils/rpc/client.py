import base64
import requests


class RPCClient(object):

    def __init__(
            self,
            host,
            auth_uri,
            username,
            password,
            rpc_uri,
            auth_host=None
    ):
        self.host = host
        self.auth_uri = auth_uri
        self.username = username
        self.password = password
        self.rpc_uri = rpc_uri
        self.auth_host = auth_host

        self.token = self.get_token()

    def prepare_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def get_token(self):
        url = self.auth_host if self.auth_host else self.host + self.auth_uri

        key = self.username
        secret = self.password

        auth_raw_string = "{}:{}".format(key, secret)
        auth_string = base64.b64encode(auth_raw_string.encode('utf-8')).decode()

        headers = {
            'Authorization': 'Basic {}'.format(auth_string)
        }

        response = requests.post(url, headers=headers)

        resj = response.json()
        access_token = resj.get('access_token')
        return access_token

    def post(self, headers, payload):
        default_headers = self.prepare_headers()
        default_headers.update(headers)
        response = requests.post(self.host + self.rpc_uri, headers=default_headers, json=payload)
        return response

    def model(self, model, method, *args, **kwargs):
        data = {
            "type": "model",
            "model": model,
            "name": method,
            "args": args,
            "kwargs": kwargs
        }
        res = self.post({}, data)
        return res

    def request(self, name, *args, **kwargs):
        data = {
            "type": "request",
            "name": name,
            "args": args,
            "kwargs": kwargs
        }
        res = self.post({}, data)
        return res


if __name__ == '__main__':
    client = RPCClient(
        "http://localhost:5000",
        "/api/auth",
        "admin",
        "admin",
        "/jsonrpc"
    )

    client.model("demo.model", 'insert_data')
    client.request("test_api")
