import requests
from .auth import Auth

class Lists:
    def __init__(self, auth: Auth):
        self.api_key = auth.api_key
        self.token = auth.token
        self.base_url = "https://api.trello.com/1/lists"

    def get_lists(self, id_board):
        """
        دریافت لیست‌های یک Board
        """
        url = f"https://api.trello.com/1/boards/{id_board}/lists"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        response = requests.get(url, params=params)
        return response.json()

    def create_list(self, name, id_board):
        """
        ایجاد یک لیست جدید در Board مشخص
        """
        url = self.base_url
        params = {
            "key": self.api_key,
            "token": self.token,
            "name": name,
            "idBoard": id_board
        }
        response = requests.post(url, params=params)
        return response.json()

    def close_list(self, id_list):
        """
        بستن یک لیست مشخص
        """
        url = f"{self.base_url}/{id_list}/closed"
        params = {
            "key": self.api_key,
            "token": self.token,
            "value": "true"
        }
        response = requests.put(url, params=params)
        return response.json()
