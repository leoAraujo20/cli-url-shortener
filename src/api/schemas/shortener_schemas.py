import ipaddress
from datetime import datetime
from urllib.parse import urlparse

from pydantic import (
    BaseModel,
    ConfigDict,
    HttpUrl,
    TypeAdapter,
    field_validator,
)
from pydantic import (
    ValidationError as PydanticValidationError,
)

from src.api.core.exceptions import InvalidURLException

http_url_adapter = TypeAdapter(HttpUrl)


class URLrequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def normalize_url(cls, value):
        if not isinstance(value, str):
            return value

        cleaned = value.strip().strip('"').strip("'").replace("\\/", "/")

        if not (cleaned.startswith("http://") or cleaned.startswith("https://")):
            cleaned = "https://" + cleaned

        return cleaned

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value):
        try:
            http_url_adapter.validate_python(value)
        except PydanticValidationError:
            raise InvalidURLException(
                value, "A URL enviada não possui um formato estrutural válido."
            )

        parsed = urlparse(value)
        hostname = parsed.hostname

        if not hostname:
            raise InvalidURLException(
                value, "A URL enviada não possui um domínio ou IP válido."
            )

        if hostname in ("localhost", "0.0.0.0"):
            raise InvalidURLException(
                value, "Não é permitido encurtar links de redes locais."
            )

        try:
            ip_obj = ipaddress.ip_address(hostname)
        except ValueError:
            pass
        else:
            if not ip_obj.is_global:
                raise InvalidURLException(
                    value, "Não é permitido encurtar endereços IP de redes privadas."
                )
        return value


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_url: str

    model_config = ConfigDict(from_attributes=True)


class ShortenResponse(URLResponse):
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
