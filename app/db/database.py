from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

if settings.USE_TEST_DB:
    db_name = settings.DB_NAME_TEST
else:
    db_name = settings.DB_NAME

MYSQL_URL = f"{settings.DB_HOST}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:" \
            f"{settings.DB_PORT}/{db_name}"

engine = create_engine(MYSQL_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def get_db():
    dbs = SessionLocal()
    try:
        yield dbs
    finally:
        dbs.close()
