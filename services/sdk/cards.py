import requests
from .auth import Auth

class Cards:
    def __init__(self, auth: Auth):
        self.api_key = auth.api_key
        self.token = auth.token
        self.base_url = "https://api.trello.com/1/cards"

    def create_card(self, name, id_list, desc=None):
        """
        ایجاد کارت جدید در لیست مشخص
        """
        url = self.base_url
        params = {
            "key": self.api_key,
            "token": self.token,
            "name": name,
            "idList": id_list,
            "desc": desc
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)

    def update_card(self, id_card, name=None, desc=None):
        """
        به‌روزرسانی اطلاعات یک کارت
        """
        url = f"{self.base_url}/{id_card}"
        params = {
            "key": self.api_key,
            "token": self.token,
        }
        if name:
            params["name"] = name
        if desc:
            params["desc"] = desc
        response = requests.put(url, params=params)
        return response.json()

    def delete_card(self, id_card):
        """
        حذف یک کارت مشخص
        """
        url = f"{self.base_url}/{id_card}"
        params = {
            "key": self.api_key,
            "token": self.token
        }
        response = requests.delete(url, params=params)
        return response.status_code == 200
    
    def get_card(self, board_id):
        """_summary_

        Args:
            board_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        url = f"https://api.trello.com/1/boards/{board_id}/cards"
        params = {
            "key": self.api_key,
            "token": self.token
        }

        # درخواست به API ترلو
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)
