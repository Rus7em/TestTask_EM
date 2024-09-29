import pytest
from httpx import AsyncClient
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .setting_test import async_db, async_client
from models.product import Product
from typing import List

product_1= {
      "name": "Stuff 1",
      "description": "stuff description",
      "price": 533.23,
      "num": 5 
}

product_2 = {
      "name": "Stuff 2",
      "description": "stuff description",
      "price": 3.23,
      "num": 23344 
}

def check_response_product(origin: dict, response: dict):
    assert response != None
    assert response["name"] == origin["name"], f"res: {response}, origin: {origin}"
    assert response["description"] == origin["description"]
    assert response["price"] == origin["price"]
    assert response["num"] == origin["num"]



def check_db_product(origin: dict, tested: Product):
    assert tested != None
    assert tested.name == origin["name"]
    assert tested.description == origin["description"]
    assert tested.price == origin["price"]
    assert tested.num == origin["num"]

def check_db_product_list(origin: list[dict], tested: Sequence[Product]):
    assert len(tested) == len(origin)
    for o in origin:
        temp_t = None
        for t in tested:
            if t.name == o["name"]:
                temp_t = t
                continue
        assert temp_t != None, f"DB doesn't have product - {o["name"]}"
        check_db_product(origin=o, tested=temp_t)

@pytest.mark.asyncio
async def test_create_product(async_client:AsyncClient, async_db: AsyncSession):
    # добавляем продукт 1 
    response = await async_client.post("/products/", json=product_1)
    assert response.status_code == 200

    # получаем id для записи продукта 1
    id = response.json()

    # читаем запись с БД
    result = await async_db.execute(select(Product).where(Product.id==id))
    db_product = result.scalar_one_or_none()
    check_db_product(origin=product_1, tested=db_product)


@pytest.mark.asyncio
async def test_get_products(async_client:AsyncClient, async_db: AsyncSession):
    # читам список продуктов при пустой БД
    response = await async_client.get("/products/" )
    assert response.status_code == 200
    assert response.json() != None

    # добавляем продукт 1 и 2 
    response = await async_client.post("/products/", json=product_1)
    assert response.status_code == 200
    response = await async_client.post("/products/", json=product_2)
    assert response.status_code == 200
    
    # читаем с бд 
    result = await async_db.execute(select(Product))
    db_product_list = result.scalars().all()
    check_db_product_list(origin=[product_1, product_2], tested=db_product_list)

@pytest.mark.asyncio
async def test_get_product(async_client:AsyncClient, async_db: AsyncSession):
    # добавляем продукт 1 и 2 
    response = await async_client.post("/products/", json=product_1)
    product_1_id = response.json()
    assert response.status_code == 200
    response = await async_client.post("/products/", json=product_2)
    assert response.status_code == 200
    product_2_id = response.json()
    
    # читаем продукт и сравниваем добавленым
    response = await async_client.get(f"/products/{product_2_id}")
    assert response.status_code == 200
    check_response_product(origin=product_2, response=response.json())
    
    response = await async_client.get(f"/products/{product_1_id}")
    assert response.status_code == 200
    check_response_product(origin=product_1, response=response.json())


@pytest.mark.asyncio
async def test_remove_product(async_client:AsyncClient, async_db: AsyncSession):
    # добавляем продукт 1 и 2 
    response = await async_client.post("/products/", json=product_1)
    product_1_id = response.json()
    assert response.status_code == 200
    response = await async_client.post("/products/", json=product_2)
    assert response.status_code == 200
    product_2_id = response.json()
    
    # читаем продукт 1
    response = await async_client.get(f"/products/{product_1_id}")
    assert response.status_code == 200
    check_response_product(origin=product_1, response=response.json())

    # удалем продекк 1 
    response = await async_client.delete(f"/products/{product_1_id}")
    assert response.status_code == 200

    # читаем продукт 1 и проверяем что нет продукта
    response = await async_client.get(f"/products/{product_1_id}")
    assert response.status_code == 404
   
    # проверяем что продукт 2 остался
    response = await async_client.get(f"/products/{product_2_id}")
    assert response.status_code == 200
    check_response_product(origin=product_2, response=response.json())


