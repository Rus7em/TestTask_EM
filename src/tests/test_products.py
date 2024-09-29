import pytest
from httpx import AsyncClient
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .setting_test import async_db, async_client
from models.product import Product
from schemas.product import ReadProduct

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

def check_response_product(origin: dict, response_product: ReadProduct):
    assert response_product != None
    assert response_product.name == origin["name"], f"res: {response_product}, origin: {origin}"
    assert response_product.description == origin["description"]
    assert response_product.price == origin["price"]
    assert response_product.num == origin["num"]



def check_db_product(origin: dict, db_product: Product):
    assert db_product!= None
    assert db_product.name == origin["name"]
    assert db_product.description == origin["description"]
    assert db_product.price == origin["price"]
    assert db_product.num == origin["num"]



def check_product_list(origin: list[dict], products: list[ReadProduct]):
    assert len(products) != None
    for o in origin:
        temp_p = None
        for p in products:
            if p.name == o["name"]:
                temp_p = p
                continue
        assert temp_p != None, f"DB doesn't have product - {o["name"]}"
        check_response_product(origin=o, response_product=temp_p)

@pytest.mark.asyncio
async def test_add_product(async_client:AsyncClient, async_db: AsyncSession):
    # добавляем продукт 1 
    response = await async_client.post("/products/", json=product_1)
    assert response.status_code == 200

    # получаем id для записи продукта 1
    id = response.json()

    # читаем запись с БД
    result = await async_db.execute(select(Product).where(Product.id==id))
    db_product = result.scalar_one_or_none()
    check_db_product(origin=product_1, db_product=db_product)


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
    
    # читаем продукты с API
    response = await async_client.get("/products/")
    assert response.status_code == 200

    product_list = [ReadProduct(**r) for r in response.json()]
    check_product_list(origin=[product_1, product_2], products= product_list)


@pytest.mark.asyncio
async def test_get_product(async_client:AsyncClient, async_db: AsyncSession):
    # добавляем продукт 1 и 2 
    response = await async_client.post("/products/", json=product_1)
    product_1_id = response.json()
    assert response.status_code == 200
    response = await async_client.post("/products/", json=product_2)
    assert response.status_code == 200
    product_2_id = response.json()
    
    # читаем продукт и сравниваем c добавленым
    response = await async_client.get(f"/products/{product_2_id}")
    assert response.status_code == 200
    check_response_product(origin=product_2, response_product=ReadProduct(**response.json()))
    
    response = await async_client.get(f"/products/{product_1_id}")
    assert response.status_code == 200
    check_response_product(origin=product_1, response_product=ReadProduct(**response.json()))


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
    check_response_product(origin=product_1, response_product=ReadProduct(**response.json()))

    # удалем продекк 1 
    response = await async_client.delete(f"/products/{product_1_id}")
    assert response.status_code == 200

    # читаем продукт 1 и проверяем что нет продукта
    response = await async_client.get(f"/products/{product_1_id}")
    assert response.status_code == 404
   
    # проверяем что продукт 2 остался
    response = await async_client.get(f"/products/{product_2_id}")
    assert response.status_code == 200


