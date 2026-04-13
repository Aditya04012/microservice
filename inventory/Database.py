from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from inventory.Models.inventory_model import Product
from user_service.Models.user_model import User
async def init_db():
    client=AsyncIOMotorClient("mongodb://localhost:27017")
    db=client["microservice"]

    await init_beanie(database=db,document_models=[Product,User])

