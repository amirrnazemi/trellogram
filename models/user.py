from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional, Annotated


class User(Document):
    telegram_id: str
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(..., description="User's email")
    trello_user_id: Optional[str] = Field(None, description="Trello user ID")
    is_active: bool = Field(default=True, description="Indicates if the user is active")

    class Settings:
        name = "users"  # Collection name in MongoDB
