from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from user_service.Models.user_model import User

async def init_db():
    cliet=AsyncIOMotorClient("mongodb://localhost:27017")
    db=cliet["microservice"]

    await init_beanie(
        database=db,document_models=[User]
    )


