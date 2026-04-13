from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException
from order_service.Models.order_model import Order
import httpx
from pydantic import BaseModel
router=APIRouter()

class OrderRequest(BaseModel):
    product_id: str
    quantity: int

class PaymentUpdateRequest(BaseModel):
    payment_intent_id: str


INVENTORY_SERVICE="http://localhost:8004"
@router.post("/")
async def order_now(request:Request,order:OrderRequest):
    email=request.headers.get("x-user-email")
    
    if not email:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    async with httpx.AsyncClient() as cliet:
        response=await cliet.post(f"{INVENTORY_SERVICE}/check-stock",json={
            "product_id":order.product_id,
            "quantity":order.quantity
        })
    
    if response.status_code!=200:
        raise HTTPException(status_code=400,detail="inventory service error")
    
    data=response.json()

    if not data.get("available"):
        raise HTTPException(status_code=400, detail="Stock not available")
    
    new_order=Order(
        user_email=email,
        product_id=order.product_id,
        quantity=order.quantity,
        status="pending_payment",
        total_price=order.quantity*data.get("price")
    )
    
    await new_order.insert()


    return {
        "message": "Order created",
        "order_id": str(new_order.id),
        "status": "pending_payment"
    }


@router.get("/my-order")
async def get_all_order(request: Request):
    email = request.headers.get("x-user-email")

    if not email:
        raise HTTPException(status_code=401, detail="User not authenticated")

    orders = await Order.find(Order.user_email == email).to_list(100)

    return {"orders": orders}


@router.get("/{order_id}")
async def get_order(order_id:str):
    order=await Order.find_one(Order.id==ObjectId(order_id))

    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    
    return order



@router.put("/{order_id}/cancel")
async def cancel_order(order_id:str):
    order=await Order.find_one(Order.id==ObjectId(order_id))
    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    
    if order.status!="pending_payment":
        raise HTTPException(status_code=400,detail="Order cannot be cancelled")
    
    order.status="cancelled"

    await order.save()


    return {"message":"Order cancelled"}



@router.put("/{order_id}/status")
async def update_order_status(order_id:str,status:str):
    order=await Order.find_one(Order.id==ObjectId(order_id))
    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    
    order.status=status

    await order.save()

    return {"message": "Order status updated"}



@router.put("/{order_id}/payment")
async def update_intend_id(order_id:str,req:PaymentUpdateRequest):
    order=await Order.find_one(Order.id==ObjectId(order_id))
    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    
    if order.status in ["paid", "refunded"]:
        raise HTTPException(status_code=400, detail="Order already completed")
    

    order.payment_intent_id=req.payment_intent_id
    order.status = "pending_payment"
    await order.save()
   
    return {"message":"Order payment intent id updated"}