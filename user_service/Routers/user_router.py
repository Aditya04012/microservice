from fastapi import APIRouter,Request,status
from fastapi import HTTPException

from jwt import InvalidTokenError,ExpiredSignatureError
from pydantic import BaseModel,EmailStr
import jwt
from bson import ObjectId
from datetime import datetime, timedelta

from user_service.Models.user_model import User


router=APIRouter()

SECRET_KEY="random key"
ALGO="HS256"
DAYS=30



class Login(BaseModel):
    email:EmailStr
    password:str

class signUp(BaseModel):
    name:str
    password:str
    email:EmailStr


@router.get("/{Id}")
async def getUserById(Id:str):
   user=await User.find_one(User.id==ObjectId(Id))
   
   
   if(not user):
      raise HTTPException(status_code=400,details="user Does not exist with this id")
   

   return {
      "message":"success",
      "user":{
         "id":str(user.id),
         "name":user.name,
         "email":user.email
      }
   }



@router.post("/signup")
async def sign_Up(req:signUp):
    name = req.name
    password = req.password
    email = req.email

    old_user=await User.find_one(User.email==email)
    if old_user:
     raise HTTPException(
        status_code=409,
        detail="User is already registered"
     )
    
    user=User(**req.dict())
    await user.insert()

    return {
        "statusCode":200,
        "message":"Register succesful plz login"
    }

def valid(pass1:str,pass2:str)->bool:
   return pass1==pass2


def create_access_token(data:dict):
   to_encode=data.copy()
   expire=datetime.utcnow()+timedelta(days=DAYS)
   to_encode.update({"exp":expire})

   token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGO)
   return token




@router.post("/login")
async def signin(req:Login):
   email=req.email 
   password=req.password
 #1) if password and email is presennt
   if not email or not password:
      raise HTTPException(status_code=400,detail="Please Provide Email and Password")
   

   #2) User exist in Db and passowrd matches
   user=await User.find_one(User.email==email)
   if(not user or not valid(user.password,password)):
      raise HTTPException(status_code=400,detail="Please Provide valid Email and Password")
   
   print(user)
   #3) create an access token
   token=create_access_token(
      data={"sub":user.email}
   )

   #4) return the token 
   return {
          "access_token":token,
           "message":"success"
           }





@router.post("protect")
async def protect_route(req:Request):
   auth_header=req.headers.get("Authorization")
   if(not auth_header or not auth_header.startswith("Bearer ")):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You Are not loged In plz login")
   
   token=auth_header.split(" ")[1]
   try:
        decode= jwt.decode(token,SECRET_KEY,algorithms=[ALGO])
        email = decode.get("sub")        
        return decode
   except ExpiredSignatureError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" expired token"
        )
   except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" Invalid token"
        )