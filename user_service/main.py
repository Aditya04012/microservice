from beanie import init_beanie
from fastapi import FastAPI

from user_service.Routers.user_router import router as user_router
from user_service.Database import init_db

app=FastAPI()


@app.on_event("startup")
async def start_db():
    await init_db()
    print("Database connected")



app.include_router(user_router,tags=['User'])