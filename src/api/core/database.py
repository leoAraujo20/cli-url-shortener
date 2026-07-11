from sqlmodel import Session, SQLModel, create_engine

import src.api.models  # noqa: F401
from src.api.core.settings import get_settings

engine = create_engine(get_settings().database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
