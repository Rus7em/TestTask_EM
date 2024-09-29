import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from database import Base, get_db
from main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(
    TEST_DATABASE_URL,
    future=True,
    echo=True
)

testing_session = async_sessionmaker(autoflush=False, bind=engine)



@pytest_asyncio.fixture(scope="function")
async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = testing_session()
    try:
        yield async_session
    finally:
        await async_session.close()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def async_client(async_db):
    def override_get_db():
        try:
            yield async_db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    ac = AsyncClient(transport=ASGITransport(app=app), base_url='http://test')
    try:
        yield ac 
    finally:
        await ac.aclose()
