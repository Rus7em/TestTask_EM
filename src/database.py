from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

DATABASE_URL = "postgresql://{}:{}@{}/{}".format(config.DB_USERNAME,
                                                 config.DB_PASSWORD,
                                                 config.DB_HOST,
                                                 config.DB_NAME)

engine = create_engine(DATABASE_URL)

session = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
