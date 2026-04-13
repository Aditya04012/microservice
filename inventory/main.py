from fastapi import FastAPI
from inventory.Database import init_db
from inventory.Router.inventory_router import router 

app=FastAPI()

@app.on_event("startup")
async def start_db():
    await init_db()
    print("Inventory Db connected")



app.include_router(router)

