=============================== MICROSERVICES BACKEND README
===============================

PROJECT OVERVIEW

This project is a scalable Microservices-based backend system built
using Fastapi,Redis ,Pydantic and MongoDB. It includes multiple services like
User, Payment, Order, and API Gateway.

Base URL: http://localhost:8000/api/v1

  ----------------------------------------
  CORE FEATURES
  ----------------------------------------
  - Microservices Architecture - API
  Gateway Pattern - JWT Authentication &
  Authorization - Role-Based Access
  Control (RBAC) - Payment Integration
  (Stripe ) - Scalable
  Folder Structure - Centralized Error
  Handling - Logging & Monitoring Ready -
  Secure REST APIs

  ----------------------------------------

PROJECT STRUCTURE

root/ │ ├── api-gateway/ │ ├── controllers/ │ ├── routes/ │ ├──
middleware/ │ └── index.js │ ├── services/ │ │ │ ├── user-service/ │ │
├── controllers/ │ │ ├── models/ │ │ ├── routes/ │ │ ├── middleware/ │ │
└── service.js │ │ │ ├── payment-service/ │ │ ├── controllers/ │ │ ├──
routes/ │ │ ├── services/ │ │ └── service.js │ │ │ ├── order-service/ │
│ ├── controllers/ │ │ ├── routes/ │ │ └── service.js │ ├── config/ ├──
utils/ ├── logs/ ├── .env └── package.json

  ------------
  API ROUTES
  ------------

BASE: http://localhost:8000/api/v1

  ---------------------
  USER SERVICE ROUTES
  ---------------------

BASE: /users

-   Register User POST /users/register

-   Login User POST /users/login Example:
    http://localhost:8000/api/v1/users/login

-   Get Profile GET /users/profile

-   Update Profile PUT /users/update

-   Delete User DELETE /users/delete

  ------------------------
  PAYMENT SERVICE ROUTES
  ------------------------

BASE: /payments

-   Create Payment POST /payments/create

-   Verify Payment POST /payments/verify

-   Payment History GET /payments/history

  ----------------------
  ORDER SERVICE ROUTES
  ----------------------

BASE: /orders

-   Create Order POST /orders/create

-   Get Orders GET /orders/

-   Get Order by ID GET /orders/:id

-   Update Order PUT /orders/:id

-   Delete Order DELETE /orders/:id

  ----------------
  AUTHENTICATION
  ----------------

-   Uses JWT Tokens
-   Send token in headers:

Authorization: Bearer

  -----------------------
  ENVIRONMENT VARIABLES
  -----------------------

PORT=8000 MONGO_URI=your_mongodb_uri JWT_SECRET=your_secret
PAYMENT_KEY=your_payment_key



  ---------------------
  FUTURE IMPROVEMENTS
  ---------------------

-   Dockerize services
-   Add Kubernetes deployment
-   Add Redis caching
-   Add CI/CD pipeline
