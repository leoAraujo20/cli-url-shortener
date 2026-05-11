from pydantic import BaseModel, field_validator


class URLrequest(BaseModel):
    url: str

    @field_validator("url", mode="before")
    @classmethod
    def normalize_url(cls, value):
        cleaned = value.strip().strip('"').strip("'")
        cleaned = cleaned.replace("\\/", "/")

        return cleaned

    @field_validator("url")
    @classmethod
    def force_only_http(cls, value):
        if not (value.startswith("http://") or value.startswith("https://")):
            value = "https://" + value
        return value


class URLresponse(BaseModel):
    id: int
    original_url: str
    short_url: str
