from fastapi import FastAPI
import asyncio

from api.v1.order import router as order_router
from api.v1.product import router as product_router

from database import engine, Base

app = FastAPI()
# app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(product_router, prefix="/products", tags=["Producs"])




