from bson import ObjectId
from fastapi import APIRouter,Request,HTTPException,status
from inventory.Models.inventory_model import Product
from pydantic import EmailStr,BaseModel
from user_service.Models.user_model import User
router=APIRouter()

async def authorized(email:EmailStr)->bool:
    user=await User.find_one(User.email==email)
    return user.role=="admin"


class StockRequest(BaseModel):
    product_id:str
    quantity:int

@router.post("/products")
async def create_new(request:Request,item:Product):
    email=request.headers.get("x-user-email")
    if(not await authorized(email)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="UnAutorized User")
    else:
        await Product.insert(item)
        return {
            "status":"success",
            "message":"Item is added to inventory"
        }


@router.get("/products")
async def getAllProduct():
    items=await Product.find_all().to_list()
    return items


@router.get("/products/{product_id}")
async def getById(product_id:str):
    item=await Product.find_one(Product.id==ObjectId(product_id))
    return item



@router.patch("/products/{id}/{quantity}")
async def update(id: str, quantity: int):
   item = await Product.find_one(Product.id == ObjectId(id))
   await item.update({"$set": {"stock": item.stock - quantity}})
   return {
        "status": "success",
        "message": "Item is Updated to inventory"
    }

@router.delete("/products/{id}")
async def deleteByid(id: str):
    product = await Product.find_one(Product.id == ObjectId(id))

    if not product:
        return {
            "status": "error",
            "message": "Product not found"
        }

    await product.delete()

    return {
        "status": "success",
        "message": "Item deleted successfully with id " + id
    }


@router.post("/check-stock")
async def check_stock(req: StockRequest):

    product = await Product.find_one(Product.id == ObjectId(req.product_id))

    if not product:
        return {"available": False}

    if product.stock < req.quantity:
        return {"available": False}

    product.stock -= req.quantity
    await product.save()

    return {"available": True, "price": product.price}