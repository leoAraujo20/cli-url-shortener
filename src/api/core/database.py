from sqlmodel import Session, create_engine

from src.api.core.settings import get_settings

engine = create_engine(get_settings().database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
