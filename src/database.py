from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


import config

DATABASE_URL = "postgresql+asyncpg://{}:{}@{}/{}".format(config.DB_USERNAME,
                                                 config.DB_PASSWORD,
                                                 config.DB_HOST,
                                                 config.DB_NAME)

engine = create_async_engine(DATABASE_URL)

session = async_sessionmaker(engine)


async def get_db():
    async with session() as s:
        yield s

Base = declarative_base()



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
