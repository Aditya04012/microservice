MICROSERVICES BACKEND PROJECT
================================

Project Type
------------
FastAPI-based microservices backend with API Gateway, JWT authentication, Redis rate limiting, MongoDB/Beanie models, order management, inventory management, and Stripe payment flow.

Base Gateway URL
-----------------
http://localhost:8000/api/v1

Service Ports
-------------
API Gateway     : http://localhost:8000
User Service    : http://localhost:8001
Order Service   : http://localhost:8002
Payment Service : http://localhost:8003
Inventory Service: http://localhost:8004

NOTE
----
Use the API Gateway URL for most requests.
For protected routes, the gateway forwards the logged-in user's email in the header:
x-user-email: <user email from JWT>

====================================================
FEATURES
====================================================
- Microservices architecture
- API Gateway with route forwarding
- User signup and login
- JWT-based authentication
- Protected routes using Authorization: Bearer <token>
- Redis-based rate limiting
- Inventory management
- Order creation and order status updates
- Stripe payment intent creation
- Refund support
- Webhook handling for Stripe events
- MongoDB / Beanie model-based storage
- Modular folder structure

====================================================
PROJECT FOLDER STRUCTURE
====================================================
```
microservices/
│
├── api_gateway/
│   ├── main.py
│   └── run.bat
│
├── user_service/
│   ├── main.py
│   ├── Database.py
│   ├── run.bat
│   ├── Models/
│   │   └── user_model.py
│   └── Routers/
│       └── user_router.py
│
├── order_service/
│   ├── main.py
│   ├── Database.py
│   ├── Models/
│   │   └── order_model.py
│   └── Routes/
│       └── order_router.py
│
├── payment_service/
│   └── main.py
│
├── inventory/
│   ├── main.py
│   ├── Database.py
│   ├── Models/
│   │   └── inventory_model.py
│   └── Router/
│       └── inventory_router.py
│
├── test.http
└── .vscode/
    └── settings.json
```

====================================================
AUTHENTICATION
====================================================
Login API returns a JWT access token.

Use token in header:
Authorization: Bearer <token>

Protected gateway routes also add:
x-user-email: <email extracted from token>

Example:
Authorization: Bearer eyJhbGciOi...
Content-Type: application/json

====================================================
API ROUTES
====================================================

1) USER SERVICE
---------------
Base via Gateway:
http://localhost:8000/api/v1/users

Public routes:

1. Signup
POST /signup
Example:
http://localhost:8000/api/v1/users/signup

Request body:
{
  "name": "Aditya",
  "email": "aditya@example.com",
  "password": "123456"
}

2. Login
POST /login
Example:
http://localhost:8000/api/v1/users/login

Request body:
{
  "email": "aditya@example.com",
  "password": "123456"
}

Response:
{
  "access_token": "<jwt_token>",
  "message": "success"
}

3. Get user by id
GET /{Id}
Example:
http://localhost:8000/api/v1/users/<user_id>

4. Protect route
POST /protect
Example:
http://localhost:8000/api/v1/users/protect

Send Authorization header with valid JWT.

Direct service URL:
http://localhost:8001

--------------------------------

2) ORDER SERVICE
-----------------
Base via Gateway:
http://localhost:8000/api/v1/orders

Protected routes require login token.

1. Create order
POST /
Example:
http://localhost:8000/api/v1/orders/

Request body:
{
  "product_id": "<product_id>",
  "quantity": 2
}

Notes:
- Reads user email from x-user-email header
- Checks inventory before creating order
- Creates order with status: pending_payment

2. Get my orders
GET /my-order
Example:
http://localhost:8000/api/v1/orders/my-order

3. Get order by id
GET /{order_id}
Example:
http://localhost:8000/api/v1/orders/<order_id>

4. Cancel order
PUT /{order_id}/cancel
Example:
http://localhost:8000/api/v1/orders/<order_id>/cancel

5. Update order status
PUT /{order_id}/status?status=paid
Example:
http://localhost:8000/api/v1/orders/<order_id>/status?status=paid

6. Update payment intent id
PUT /{order_id}/payment
Example:
http://localhost:8000/api/v1/orders/<order_id>/payment

Request body:
{
  "payment_intent_id": "pi_123"
}

Direct service URL:
http://localhost:8002

--------------------------------

3) PAYMENT SERVICE
-------------------
Base via Gateway:
http://localhost:8000/api/v1/payments

1. Create payment intent
POST /create-payment-intent
Example:
http://localhost:8000/api/v1/payments/create-payment-intent

Request body:
{
  "order_id": "<order_id>"
}

Flow:
- Fetches order from order service
- Validates order status is pending_payment
- Creates Stripe payment intent
- Updates order with payment_intent_id

Response:
{
  "client_secret": "<stripe_client_secret>"
}

2. Refund payment
POST /refund
Example:
http://localhost:8000/api/v1/payments/refund

Request body:
{
  "order_id": "<order_id>"
}

3. Stripe webhook
POST /webhook
Example:
http://localhost:8000/api/v1/payments/webhook

Handled events:
- payment_intent.succeeded
- payment_intent.payment_failed
- charge.refunded
- payment_intent.processing

4. Health check
GET /
Example:
http://localhost:8000/api/v1/payments/

Direct service URL:
http://localhost:8003

--------------------------------

4) INVENTORY SERVICE
--------------------
Base via Gateway:
http://localhost:8000/api/v1/inventory

1. Create product
POST /products
Example:
http://localhost:8000/api/v1/inventory/products

Note:
- Admin-only route
- Reads x-user-email header

Request body depends on Product model.

2. Get all products
GET /products
Example:
http://localhost:8000/api/v1/inventory/products

3. Get product by id
GET /products/{product_id}
Example:
http://localhost:8000/api/v1/inventory/products/<product_id>

4. Update stock
PATCH /products/{id}/{quantity}
Example:
http://localhost:8000/api/v1/inventory/products/<id>/2

5. Delete product
DELETE /products/{id}
Example:
http://localhost:8000/api/v1/inventory/products/<id>

6. Check stock
POST /check-stock
Example:
http://localhost:8000/api/v1/inventory/check-stock

Request body:
{
  "product_id": "<product_id>",
  "quantity": 2
}

Response:
{
  "available": true,
  "price": 1000
}

Direct service URL:
http://localhost:8004

====================================================
API GATEWAY BEHAVIOR
====================================================
Gateway file:
api_gateway/main.py

Routes:
- /api/v1/users/{path}
  Public proxy for user service

- /api/v1/{service}/{path}
  Proxy for protected services:
  - orders
  - payments
  - inventory

Gateway responsibilities:
- route forwarding
- rate limiting via Redis
- token validation
- adding x-user-email header to protected service calls

====================================================
ENVIRONMENT VARIABLES
====================================================
Suggested variables:

PORT=8000
MONGO_URI=your_mongodb_uri
JWT_SECRET=your_jwt_secret
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
REDIS_HOST=localhost
REDIS_PORT=6379

====================================================
HOW TO RUN
====================================================
1. Install dependencies for each service
   pip install -r requirements.txt

2. Start MongoDB and Redis

3. Run services one by one:
   - user service
   - order service
   - inventory service
   - payment service
   - api gateway

4. Test using Postman or the test.http file

====================================================
EXAMPLE REQUEST FLOW
====================================================
1. Sign up a user
   POST http://localhost:8000/api/v1/users/signup

2. Login user
   POST http://localhost:8000/api/v1/users/login

3. Create an order with JWT token
   POST http://localhost:8000/api/v1/orders/

4. Create payment intent
   POST http://localhost:8000/api/v1/payments/create-payment-intent

5. Stripe webhook updates order status automatically


