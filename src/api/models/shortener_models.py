from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

from src.api.core.database import engine


class URL(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    original_url: str


class URLAccess(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url_id: int = Field(foreign_key="url.id")
    accessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_agent: str | None = None
    referrer: str | None = None
    ip_address: str | None = None


SQLModel.metadata.create_all(engine)
