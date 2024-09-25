from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from schemas.product import CreateProduct
from models.product import Product


async def add_product(product: CreateProduct, db: AsyncSession):
    db_product = Product(name=product.name,
                         description=product.description,
                         price=product.price,
                         num=product.num)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_product_list(db: AsyncSession):
    # добавить пагинацию
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product(id: int, db: AsyncSession):
    result = await db.execute(select(Product).where(Product.id==id))
    db_product = result.scalars().first()
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_product

async def edit_product(id:int, product: CreateProduct, db: AsyncSession):
    result = await db.execute(select(Product).where(Product.id==id))
    db_product = result.scalars().first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.num = product.num 

    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(id:int, db: AsyncSession):
    result = await db.execute(select(Product).where(Product.id==id))
    db_product = result.scalars().first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(db_product)
    await db.commit()
    return
