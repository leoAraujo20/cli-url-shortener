from sqlmodel import Field, SQLModel

from src.api.core.database import engine


class URL(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    original_url: str


SQLModel.metadata.create_all(engine)
