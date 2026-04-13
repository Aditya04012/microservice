from pydantic import EmailStr
from beanie import Document
class User(Document):
    name:str
    email:str
    password:str
    role: str = "user"

    class Settings:
        name = "users"

