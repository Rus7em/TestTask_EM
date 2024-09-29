import pytest
from httpx import AsyncClient
from typing import Sequence, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .setting_test import async_db, async_client
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from tests import test_products 
from schemas.order import ReadOrder, ReadOrderItem

test_order = {
    "status": "Processing",
    "items": []
}

test_order_item: Dict[str, Any] = {
    "product_id": None,
    "num": None
}


def check_db_order_item(origin: dict, db_order_item: OrderItem):
    assert db_order_item.product_id == origin["product_id"]
    assert db_order_item.num == origin["num"]


def check_db_order(origin: dict, db_order: Order):
    assert db_order.status == origin["status"]

def check_db_order_item_list(origin: list[dict], db_order_item_list: Sequence[OrderItem]):
    assert len(db_order_item_list) == len(origin)
    for item_tested  in db_order_item_list:
        temp_origin_item = None
        for item_origin in origin:
            if item_tested.product_id == item_origin["product_id"]:
                temp_origin_item = item_origin
                continue
        assert temp_origin_item != None, f"product '{item_tested.product_id}' not in order"
        check_db_order_item(origin=temp_origin_item, db_order_item=item_tested)


def check_response_order(origin: dict, response_order: ReadOrder):
    assert response_order.status == origin["status"]
    assert response_order.items != None
    for o_item in origin["items"]:
        temp_response_item = None
        for r_item in response_order.items:
            if r_item.product_id == o_item["product_id"]:
                temp_response_item = r_item
                continue
        assert temp_response_item != None

@pytest.mark.asyncio
async def test_add_order(async_client:AsyncClient, async_db: AsyncSession):
    #добавляем продукты
    # добавляем продукт 1 и 2 
    response = await async_client.post("/products/", json=test_products.product_1)
    assert response.status_code == 200
    product_1_id = response.json()
    response = await async_client.post("/products/", json=test_products.product_2)
    assert response.status_code == 200
    product_2_id = response.json()

    # создаем ордер
    req_order = test_order.copy()
    req_order_item_1 = test_order_item.copy()
    req_order_item_2 = test_order_item.copy()
    req_order_item_1["product_id"] = product_1_id
    req_order_item_1["num"] = 2
    req_order_item_2["product_id"] = product_2_id
    req_order_item_2["num"] = 2
    req_order["items"] = [req_order_item_1, req_order_item_2]
    response = await async_client.post("/orders/", json=req_order)
    assert response.status_code == 200
    id = response.json() # id ордера

    # читаем данные из БД ордер
    result = await async_db.execute(select(Order).where(Order.id==id))
    order_data = result.scalar_one_or_none()
    assert order_data != None
    check_db_order(origin=req_order, db_order=order_data)
    
    # читаем данные из БД order items 
    result = await async_db.execute(select(OrderItem).where(OrderItem.order_id==id))
    order_item_list = result.scalars().all()
    check_db_order_item_list(origin=req_order["items"], db_order_item_list=order_item_list)



@pytest.mark.asyncio
async def test_get_order(async_client:AsyncClient, async_db: AsyncSession):
    #добавляем продукты
    # добавляем продукт 1 и 2 
    response = await async_client.post("/products/", json=test_products.product_1)
    assert response.status_code == 200
    product_1_id = response.json()
    response = await async_client.post("/products/", json=test_products.product_2)
    assert response.status_code == 200
    product_2_id = response.json()

    # создаем ордер 1
    req_order = test_order.copy()
    req_order_item_1 = test_order_item.copy()
    req_order_item_2 = test_order_item.copy()
    req_order_item_1["product_id"] = product_1_id
    req_order_item_1["num"] = 2
    req_order_item_2["product_id"] = product_2_id
    req_order_item_2["num"] = 100
    req_order["items"] = [req_order_item_1, req_order_item_2]
    response = await async_client.post("/orders/", json=req_order)
    assert response.status_code == 200
    order_id = response.json()

    
    # читаем ордер с API 
    response = await async_client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    response_order= ReadOrder(**response.json()) 
    check_response_order(origin=req_order, response_order=response_order)



@pytest.mark.asyncio
async def test_set_status(async_client:AsyncClient, async_db: AsyncSession):
    #добавляем продукты
    # добавляем продукт 1 и 2 
    response = await async_client.post("/products/", json=test_products.product_1)
    assert response.status_code == 200
    product_1_id = response.json()
    response = await async_client.post("/products/", json=test_products.product_2)
    assert response.status_code == 200
    product_2_id = response.json()

    # создаем ордер 1
    req_order = test_order.copy()
    req_order_item_1 = test_order_item.copy()
    req_order_item_2 = test_order_item.copy()
    req_order_item_1["product_id"] = product_1_id
    req_order_item_1["num"] = 2
    req_order_item_2["product_id"] = product_2_id
    req_order_item_2["num"] = 100
    req_order["items"] = [req_order_item_1, req_order_item_2]
    response = await async_client.post("/orders/", json=req_order)
    assert response.status_code == 200
    order_id = response.json()

   
    # читаем ордер с API 
    new_status = "Shipped"
    response = await async_client.patch(f"/orders/{order_id}/status?status={new_status}")
    assert response.status_code == 200

    result = await async_db.execute(select(Order).where(Order.id==order_id))
    db_order = result.scalar_one_or_none()
    assert db_order != None
    assert db_order.status == new_status




