from fastapi import FastAPI

from api.v1.order import router as order_router
from api.v1.product import router as product_router


app = FastAPI()

app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(product_router, prefix="/products", tags=["Producs"])
