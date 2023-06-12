from fastapi import APIRouter, Depends, Response
from beanie import PydanticObjectId, exceptions
from typing import List
from src.auth.users import current_active_user
from src.models import User, Chat, IdName
from src.schemas import CreateChat

router = APIRouter()


@router.get("/users", response_model=List[IdName])
async def get_users():
    users = await User.find_all().to_list()
    return [IdName(id=user.id, name=user.name) for user in users]


@router.get("/chats")
async def get_chats(user: User = Depends(current_active_user)):
    return user.chats


@router.post("/chats")
async def create_chat(pyload: CreateChat, user: User = Depends(current_active_user)):
    second_user = await User.get(pyload.second_user_id)
    if second_user:
        user_id_name = IdName(id=user.id, name=user.email)
        second_user_id_name = IdName(id=second_user.id, name=second_user.email)
        chat = Chat(name=pyload.chat_name, owner=user_id_name, participants=[user_id_name, second_user_id_name])
        try:
            await chat.create()
            chat_id_name = IdName(id=chat.id, name=chat.name)
            user.chats.append(chat_id_name)
            second_user.chats.append(chat_id_name)
            await user.save()
            await second_user.save()
            return Response(status_code=200)
        except (exceptions.StateNotSaved, exceptions.DocumentWasNotSaved):
            user.rollback()
            second_user.rollback()
            chat.rollback()
            return Response("Failed to create a chat, try again later.", status_code=400)
    return Response("Failed to create chat, user does not exist.", status_code=400)


@router.get("/chats/{chat_id}", response_model=Chat)
async def get_chat(chat_id: PydanticObjectId, user: User = Depends(current_active_user)):
    chat = await Chat.get(chat_id)
    if chat and user.id in [user.id for user in chat.participants]:
        return chat
    return Response(status_code=404)


@router.post("/chats/{chat_id}")
async def add_user_in_chat(
        chat_id: PydanticObjectId,
        second_user_id: PydanticObjectId,
        user: User = Depends(current_active_user)
):
    second_user = await User.get(second_user_id)
    if second_user:
        chat = await Chat.get(chat_id)
        if chat and user.id == chat.owner.id and second_user not in chat.participants:
            second_user_id_name = IdName(id=second_user.id, name=second_user.email)
            chat_id_name = IdName(id=chat.id, name=chat.name)
            chat.participants.append(second_user_id_name)
            second_user.chats.append(chat_id_name)
            try:
                await chat.save()
                await second_user.save()
                return Response(status_code=200)
            except (exceptions.StateNotSaved, exceptions.DocumentWasNotSaved):
                second_user.rollback()
                chat.rollback()
    return Response("Failed to add a user to the chat.", status_code=400)


@router.get("/messages")
async def get_messages(): pass


@router.post("/messages")
async def create_message(): pass

