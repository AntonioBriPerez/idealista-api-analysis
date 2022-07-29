import base64
import os
import requests


class Idealista:
    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret
        self.base64 = base64.b64encode(
            f"{self.api_key}:{self.secret}".encode()
        ).decode()
        self.access_token = self.get_access_token()

    def __str__(self) -> str:
        return f"API KEY {self.api_key}  \nSecret: {self.secret} \nBase64: {self.base64}\nAccess token: {self.access_token}"

    def get_access_token(self):
        api_headers = {
            "Authorization": f"Basic {self.base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return requests.post(
            url="https://api.idealista.com/oauth/token",
            data="grant_type=client_credentials&scope=read",
            headers=api_headers,
            verify=False,
        ).json()["access_token"]

    def make_request(self, kind) -> str:
        if kind == "GET":
            pass
        elif kind == "POST":
            headers_dic = {
                "Authorization": "Bearer " + self.access_token,
                "Content-Type": "application/x-www-form-urlencoded",
            }

            params_dic = {
                "operation": "rent",
                "locationId": "0-EU-ES-01",
                "propertyType": "homes",
            }

            r = requests.post(
                "https://api.idealista.com/3.5/es/search",
                headers=headers_dic,
                params=params_dic,
            )

            return r.text

        else:
            raise ValueError(f"{kind} no es un tipo valido de petición")


def main():
    def read_idealista_secrets(keys_path):
        with open(os.path.join(keys_path, "api_key")) as f:
            key = f.readline()
        with open(os.path.join(keys_path, "secret")) as f:
            secret = f.readline()
        return key, secret

    idealista = Idealista(
        *read_idealista_secrets(f"{os.path.expanduser('~')}/.idealista_keys")
    )
    print(idealista.make_request("POST"))


if __name__ == "__main__":
    main()
