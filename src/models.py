from beanie import Document, PydanticObjectId
from fastapi_users.db import BeanieBaseUser
from pydantic import BaseModel
from typing import List
from datetime import datetime


class IdName(BaseModel):
    id: PydanticObjectId
    name: str


class User(BeanieBaseUser, Document):
    name: str
    chats: List[IdName] = []


class Chat(Document):
    name: str
    owner: IdName
    participants: List[IdName]

    class Settings:
        name = "chat"


class Message(Document):
    sender: IdName
    chat: IdName
    datetime: str
    text: str
    is_read: bool = False

    class Settings:
        name = "message"
