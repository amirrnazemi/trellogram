# services/trello_service.py

import aiohttp
from config import TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID

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
            
        for key in params.keys():
            if isinstance(params[key], list):
                params[key] = ",".join(params[key])
            
        return params
    
    async def get_members(self, board_id: str = TRELLO_BOARD_ID):
        url = f"{self.BASE_URL}/boards/{board_id}/members"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params()) as response:
                response.raise_for_status()
                return await response.json()
    
    async def get_boards(self, user_id: str = "me", query_params={}):
        url = f"{self.BASE_URL}/members/{user_id}/boards"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params(query_params)) as response:
                response.raise_for_status()
                return await response.json()
            
    async def get_my_boards(self, query_params=None):
        url = f"{self.BASE_URL}/members/me/boards"
        
        if query_params is None:
            query_params = {}
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params(query_params)) as response:
                response.raise_for_status()
                return await response.json()
            
    async def get_my_open_boards(self, query_params=None):
        url = f"{self.BASE_URL}/members/me/boards"
        
        if query_params is None:
            query_params = {}
            
        if "fields" in query_params:
            if not isinstance(query_params["fields"], list):
                fields = query_params["fields"].split(",")
            else:
                fields = query_params["fields"]
                
            if "closed" not in fields:
                fields.append("closed")
                query_params['fields'] = fields

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params(query_params)) as response:
                response.raise_for_status()
                
                boards = await response.json()
                
                return list(filter(lambda board: not board.get('closed', True), boards))
        
    async def get_tasks(self, board_id: str = TRELLO_BOARD_ID, query_params=None):
        url = f"https://api.trello.com/1/boards/{board_id}/cards"
        
        if query_params is None:
            query_params = []
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params()) as response:
                response.raise_for_status()
                return await self.__get_custom_fields(await response.json(), query_params['fields'])
    
    async def get_open_tasks(self, board_id: str = TRELLO_BOARD_ID, query_params=None):
        url = f"https://api.trello.com/1/boards/{board_id}/cards"
        
        if query_params is None:
            query_params = []
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params({'filter':'open'})) as response:
                response.raise_for_status()
                return await self.__get_custom_fields(await response.json(), query_params['fields'])
    
    async def __get_custom_fields(self, obj, query_params=[]):
        if not query_params:
            return obj
        else:
            if isinstance(obj, list):
                new_objs = []
                for _obj in obj:
                    temp = {}
                    for query in query_params:
                        temp[query] = _obj.get(query, None)
                    new_objs.append(temp)
                return new_objs
            else:
                new_obj = {}
                for query in query_params:
                    new_objs = obj.get(query)
                return new_obj
            
                
    # سایر متدهای مورد نیاز برای تعامل با Trello API به صورت async

    ########################################################
    async def get_lists(self, board_id = TRELLO_BOARD_ID, query_params=[]):
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        
        if query_params is None:
            query_params = []
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=self._get_params(query_params)) as response:
                response.raise_for_status()
                return await response.json()