from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
