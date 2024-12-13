from beanie import Document, Indexed
from pydantic import Field
from typing import Optional, Annotated


class Bot(Document):
    is_active: bool = Field(default=True)
    last_lists_update: str
    last_boards_upate: str
    last_cards_update: str
    
    

    class Settings:
        name = "bot_settings"  # Collection name in MongoDB
