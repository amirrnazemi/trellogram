from beanie import Document
from pydantic import Field

class MapList(Document):
    name: str = Field(..., description="Name of the list")
    trello_list_id: str = Field(..., description="Trello list ID")
    mapped_category: str = Field(..., description="Mapped category in the bot")
    
    class Settings:
        name = "map_lists"  # MongoDB collection name
        indexes = [
            {"fields": ["trello_list_id"], "unique": True}  # Unique index on 'trello_list_id'
        ]
