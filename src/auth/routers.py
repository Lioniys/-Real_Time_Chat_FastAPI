from fastapi import APIRouter, Depends
from src.auth.schemas import UserCreate, UserRead
from src.auth.users import auth_backend, fastapi_users, current_active_user
from src.models import User


router = APIRouter()
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))


@router.get("/verify")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {}
