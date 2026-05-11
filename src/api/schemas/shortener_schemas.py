from pydantic import BaseModel, field_validator


class URLrequest(BaseModel):
    url: str

    @field_validator("url", mode="before")
    @classmethod
    def normalize_url(cls, value):
        cleaned_value = value.strip().replace("\\", "")
        return cleaned_value


class URLresponse(BaseModel):
    id: int
    original_url: str
    short_url: str
