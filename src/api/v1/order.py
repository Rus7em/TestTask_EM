from fastapi import APIRouter, Depends, Query, Body, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from schemas.order import CreateOrder, ReadOrder, Status
from schemas.order_item import CreateOrderItem, ReadOrderItem
from models.order import Order
from models.order_item import OrderItem
import service 
from database import get_db


router = APIRouter()

async def order_item_parameter(product_id: int, num: int):
    return {"product_id": product_id, "num": num}

order_item_dep = Annotated[dict, Depends(order_item_parameter)]

async def order_parameters(status: int, order_items:List[order_item_dep]):
    return {"status": status, "order_items": order_items}

order_dep = Annotated[dict, Depends(order_parameters)]


@router.post("/", response_model=int)
async def add_order(order: CreateOrder, db: AsyncSession = Depends(get_db)):
    return await service.add_order(order=order, db=db)

@router.get("/", response_model=List[ReadOrder])
async def get_order_list(db: AsyncSession = Depends(get_db)):
    return await service.get_order_list(db=db)

@router.get("/{id}", response_model=ReadOrder)
async def get_order(id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_order(id=id, db=db)

@router.patch("/{id}/status")
async def set_order_status(id: int, status: Status, db: AsyncSession = Depends(get_db)):
    return await service.set_status(id=id, status=status, db=db)
