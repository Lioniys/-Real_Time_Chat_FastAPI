from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from src.database import db
from src.models import User, Chat, Message
from src.auth.routers import router as auth_router
from src.routers import router


app = FastAPI(title="ChatAPI")

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    await init_beanie(database=db, document_models=[User, Chat, Message])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
