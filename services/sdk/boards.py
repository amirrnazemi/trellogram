import requests
from .auth import Auth


class Boards:
    def __init__(self, auth: Auth):
        self.api_key = auth.api_key
        self.token = auth.token
        self.base_url = "https://api.trello.com/1"

    def get_boards(self):
        url = f"{self.base_url}/members/me/boards"
        params = {"key": self.api_key, "token": self.token}
        response = requests.get(url, params=params)
        return response.json()
