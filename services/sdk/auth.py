


class Auth:
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token

    def get_credentials(self):
        return {"key": self.api_key, "token": self.token}
