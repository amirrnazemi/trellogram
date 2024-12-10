from beanie import Document, Link
from pydantic import Field
from typing import Optional
from models.map_list import Map_List

class Map_Card(Document):
    title: str = Field(...)
    description: Optional[str] = Field(...)
    completed: str = Field(...)
    list: Link[Map_List]
    
    class Settings:
        name = "map_cards" 
        indexes = [
            'title',
        ]
