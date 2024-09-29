from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Dict

from schemas.product import CreateProduct
from models.product import Product
from schemas.order import CreateOrder, ReadOrder, Status
from schemas.order_item import CreateOrderItem, ReadOrderItem
from models.order import Order
from models.order_item import OrderItem


async def add_product(product: CreateProduct, db: AsyncSession):
    db_product = Product(name=product.name,
                         description=product.description,
                         price=product.price,
                         num=product.num)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product.id

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

async def add_order(order: CreateOrder, db: AsyncSession):
    ## Создание уникального набора продуктов и их сумарным количеством позиций (Нужно для проверки наличия).
    uniq_items: Dict[int, CreateOrderItem] = {}
    for item in order.items:
        if item.product_id in uniq_items:
            uniq_items[item.product_id].num += item.num
        else:
            uniq_items[item.product_id] = item

    #Проверка наличия товара 
    db_product_dict: Dict[int, Product] = {}
    for p in uniq_items.values():
        result = await db.execute(select(Product).where(Product.id==p.product_id))
        db_product = result.scalars().first()
        if db_product is None:
            raise HTTPException(status_code=404, detail=f"Product not found with id={p.product_id}")
        if db_product.num < p.num:
            raise HTTPException(status_code=404, detail=f"The quantity of product {db_product.name} is not enough")
        # сохранение объектов моделей продуктов, для последующего вычета 
        if p.product_id not in db_product_dict:
            db_product_dict[p.product_id] = db_product
            db.expunge(db_product)



    #Создание заказа
    db_order = Order(status=order.status)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    for item in order.items:
        db_item = OrderItem(order_id=db_order.id, product_id=item.product_id, num=item.num)
        db.add(db_item)
        # вычетание продуктов из наличия
        print("----", db_product_dict)
        print("----", item.product_id)
        print("----", db_product_dict[item.product_id].num)

        db_product_dict[item.product_id].num -= item.num
    
    for db_product in db_product_dict.values():
        db.add(db_product)

    await db.commit()
    await db.refresh(db_order)
    return db_order.id


async def get_order_list(db: AsyncSession) -> List[ReadOrder]:
    result_orders = await db.execute(select(Order))
    order_list: List[ReadOrder] = []
    for o in result_orders.scalars().all():
        order = ReadOrder.model_validate(o)
        result_items = await db.execute(select(OrderItem).where(OrderItem.order_id==order.id))
        order.items = []
        for i in result_items.scalars().all():
            item = ReadOrderItem.model_validate(i)
            order.items.append(item)
        order_list.append(order)
    return order_list



async def get_order(id: int, db: AsyncSession):
    result = await db.execute(select(Order).where(Order.id==id))
    db_order = result.scalars().first()

    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    order = ReadOrder.model_validate(db_order)
    result_items = await db.execute(select(OrderItem).where(OrderItem.order_id==order.id))
    order.items = []
    for i in result_items.scalars().all():
        item = ReadOrderItem.model_validate(i)
        order.items.append(item)
    return order

async def set_status(id: int, status: Status, db: AsyncSession):
    result = await db.execute(select(Order).where(Order.id==id))
    db_order = result.scalars().one_or_none()

    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = status
    await db.commit()
