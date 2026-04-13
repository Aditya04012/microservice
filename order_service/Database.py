from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from order_service.Models.order_model import Order



async def init_db():
    client=AsyncIOMotorClient("mongodb://localhost:27017")
    db=client["microservice"]

    await init_beanie(database=db,document_models=[Order])