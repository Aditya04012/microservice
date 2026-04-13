from fastapi import FastAPI,Request,Depends
from pydantic import BaseModel
from jwt import ExpiredSignatureError,InvalidTokenError,InvalidSignatureError
from fastapi.exceptions import HTTPException
import httpx
from user_service.Models.user_model import User
from user_service.Routers.user_router import protect_route
import redis
import time

r=redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

RATE_LIMIT=5
WINDOW=10

def rate_limiter(request:Request):
    ip=request.client.host

    key = f"rate_limit:{ip}"
    current = r.get(key)

    if current:
        if int(current) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests")
        else:
            r.incr(key)
    else:
        r.set(key, 1, ex=WINDOW)



SERVICES = {
    "users": "http://localhost:8001",
    "orders": "http://localhost:8002",
    "payments": "http://localhost:8003",
    "inventory":"http://localhost:8004"
}




app=FastAPI()


@app.api_route("/api/v1/users/{path:path}",methods=["GET","POST","PUT","DELETE","PATCH"])
async def User(path:str,req:Request,rl=Depends(rate_limiter)):

    
    async with httpx.AsyncClient() as client:
        response=await client.request(
        method=req.method,
        url=f"{SERVICES['users']}/{path}",
        headers=dict(req.headers),
        content=await req.body()
        )
    
    return response.json()


@app.api_route("/api/v1/{service}/{path:path}",methods=["GET","POST","PUT","DELETE","PATCH"])
async def getway(service:str,path:str,req:Request,user=Depends(protect_route),rl=Depends(rate_limiter)):

    if service not in SERVICES:
        return {"error": "Service not found"}
    
    headers = dict(req.headers)
    headers["x-user-email"] = user["sub"]
    
    

    async with httpx.AsyncClient() as client:
        response=await client.request(
            method=req.method,
            url=f"{SERVICES[service]}/{path}",
            headers=headers,
            content=await req.body()
        )
    return response.json()