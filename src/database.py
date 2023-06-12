import motor.motor_asyncio
from fastapi_users.db import BeanieUserDatabase
from src.settings import DATABASE_URL, DATABASE_NAME
from src.models import User

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL, uuidRepresentation="standard")
db = client[DATABASE_NAME]


async def get_user_db():
    yield BeanieUserDatabase(User)
