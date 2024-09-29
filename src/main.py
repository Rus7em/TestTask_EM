from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.v1.order import router as order_router
from api.v1.product import router as product_router
from database import init_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(product_router, prefix="/products", tags=["Producs"])
