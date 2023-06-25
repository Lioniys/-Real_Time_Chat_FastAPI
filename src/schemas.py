from pydantic import BaseModel
from beanie import PydanticObjectId


class CreateChat(BaseModel):
    chat_name: str
    second_user_id: PydanticObjectId
