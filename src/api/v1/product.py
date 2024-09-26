from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from schemas.product import CreateProduct, ReadProduct
import service
from database import get_db

router = APIRouter()

async def product_parameters(name: str, description: str, price: str, num: int):
    return {"name": name, "description": description, "price": price, "num": num}

product_dep = Annotated[dict, Depends(product_parameters)]


@router.post("/", response_model=ReadProduct)
async def add(product: CreateProduct = Body(...), db: AsyncSession = Depends(get_db)):
    return await service.add_product(product=product, db=db)

@router.get("/", response_model=List[ReadProduct])
async def get_list(db: AsyncSession = Depends(get_db)):
    return await service.get_product_list(db=db)

@router.get("/{id}", response_model=ReadProduct)
async def get(id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_product(id=id, db=db)

@router.put("/{id}", response_model=ReadProduct)
async def edit(id: int, parameters: product_dep, db: AsyncSession = Depends(get_db)):
    product = CreateProduct(**parameters)
    return await service.edit_product(id=id, product=product, db=db)

@router.delete('/{id}')
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    return await service.delete_product(id=id, db=db)
