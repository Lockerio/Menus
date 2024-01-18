from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import config


engine = create_engine(config.DATABASE_URL)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

