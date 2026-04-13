    from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel
import httpx
import stripe



app=FastAPI()

stripe.api_key="____"
endpoint_secret = "whsec_XXXX"
ORDER_SERVICE="http://localhost:8002"

class PaymentModel(BaseModel):
    order_id:str



@app.post('/create-payment-intent')
async def create_payment(req:PaymentModel):

    async with httpx.AsyncClient() as client:
        response=await client.get(f"{ORDER_SERVICE}/{req.order_id}")
    
    if response.status_code!=200:
        raise HTTPException(status_code=404,detail="order not found")
    
    order=response.json()
    
    if(order['status']!="pending_payment"):
        raise HTTPException(status_code=400,detail="Invalid order status")
    
    amount=int(order["total_price"]*100)


    intent=stripe.PaymentIntent.create(
        amount=amount,
        currency="inr",
        metadata={"order_id":req.order_id}
    )


    async with httpx.AsyncClient() as client:
        await client.put(
        f"{ORDER_SERVICE}/{req.order_id}/payment",
        json={"payment_intent_id": intent.id}
    )

    return {
        "client_secret":intent.client_secret
    }



@app.post("/refund")
async def get_refund(req: PaymentModel):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE}/{req.order_id}")
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="No order found")
    
    order = response.json()

    if order["status"] != "paid":
        raise HTTPException(status_code=400, detail="Only paid order can be refunded")
    
    payment_intent_id = order.get("payment_intent_id")

    refund = stripe.Refund.create(
        payment_intent=payment_intent_id
    )

    return {
        "refund_id": refund.id,
        "status": refund.status
    }
    
@app.post("/webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

   
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook error")

    event_type = event["type"]

    
    try:

        
        if event_type == "payment_intent.succeeded":

            intent = event["data"]["object"]
            order_id = intent["metadata"]["order_id"]

            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.put(
                    f"{ORDER_SERVICE}/{order_id}/status",
                    params={"status": "paid"}
                )

        
        elif event_type == "payment_intent.payment_failed":

            intent = event["data"]["object"]
            order_id = intent["metadata"]["order_id"]

            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.put(
                    f"{ORDER_SERVICE}/{order_id}/status",
                    params={"status": "failed"}
                )

       
        elif event_type == "charge.refunded":

            charge = event["data"]["object"]
            payment_intent_id = charge["payment_intent"]

            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.put(
                    f"{ORDER_SERVICE}/payment/{payment_intent_id}/status",
                    params={"status": "refunded"}
                )

      
        elif event_type == "payment_intent.processing":

            intent = event["data"]["object"]
            order_id = intent["metadata"]["order_id"]

            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.put(
                    f"{ORDER_SERVICE}/{order_id}/status",
                    params={"status": "pending_payment"}
                )

    except Exception as e:
        
        print("Webhook handling error:", str(e))
        raise HTTPException(status_code=500, detail="Webhook processing failed")

    return {"status": "success"}



"""
Call /create-payment-intent

Get client_secret

Use Stripe JS:

await stripe.confirmCardPayment(client_secret, {
  payment_method: {
    card: cardElement,
  }
});
"""

@app.get("/")
def get():
    return {"server is running payemnt"}