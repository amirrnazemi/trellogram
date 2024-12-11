from beanie import Document, Indexed
from typing import Annotated
from pydantic import Field

class Map_List(Document):
    name: str = Field(..., description="Name of the list")
    trello_list_id: Annotated[str, Indexed(unique=True)] = Field(..., description="Trello list ID")
    mapped_category: str = Field(..., description="Mapped category in the bot")
    
    class Settings:
        name = "map_lists"  # MongoDB collection name

