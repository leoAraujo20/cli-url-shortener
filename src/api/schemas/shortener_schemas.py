from datetime import datetime
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, field_validator

from src.api.core.exceptions import InvalidURLException


class URLrequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def valdiate_url(cls, value):
        if not (value.startswith("http://") or value.startswith("https://")):
            value = "https://" + value
        parsed = urlparse(value)
        if not parsed.netloc:
            raise InvalidURLException(value, "A URL enviada não é válida")
        return value

    @field_validator("url", mode="before")
    @classmethod
    def normalize_url(cls, value):
        cleaned = value.strip().strip('"').strip("'")
        cleaned = cleaned.replace("\\/", "/")

        return cleaned


class URLresponse(BaseModel):
    id: int
    original_url: str
    short_url: str
    message: str


class AccessRecord(BaseModel):
    accessed_at: datetime
    user_agent: str | None
    referrer: str | None
    ip_address: str | None

    model_config = ConfigDict(from_attributes=True)


class URLStatsResponse(BaseModel):
    original_url: str
    short_url: str
    total_accesses: int
    top_referrers: dict[str, int]
    unique_visitors: int
    recent_accesses: list[AccessRecord]
