# services/trello_service.py

import aiohttp
from config import TRELLO_API_KEY, TRELLO_TOKEN

class TrelloClient:
    BASE_URL = "https://api.trello.com/1"
    
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
    
    def _get_params(self, additional_params=None):
        params = {
            "key": self.api_key,
            "token": self.token
        }
        if additional_params:
            params.update(additional_params)
        return params
    
    async def get_members(self, board_id: str = None):
        if board_id:
            url = f"{self.BASE_URL}/boards/{board_id}/members"
        else:
            url = f"{self.BASE_URL}/members/me/boards"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params()) as response:
                response.raise_for_status()
                return await response.json()
    
    async def get_boards(self, user_id: str = "me"):
        url = f"{self.BASE_URL}/members/{user_id}/boards"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params()) as response:
                response.raise_for_status()
                return await response.json()
    
    # سایر متدهای مورد نیاز برای تعامل با Trello API به صورت async
