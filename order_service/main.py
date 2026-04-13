from fastapi import FastAPI
from order_service.Database import init_db
from order_service.Routes.order_router import router
app=FastAPI()




@app.on_event("startup")
async def start_db():
    await init_db()
    print("order DB connected")


app.include_router(router)