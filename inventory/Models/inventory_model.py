from pydantic import BaseModel
from beanie import Document

class Product(Document):
    name:str
    description:str
    price:float
    stock:int
    category:str

    class Settings:
        name = "products"