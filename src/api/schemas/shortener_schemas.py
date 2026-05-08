from pydantic import BaseModel


class URLrequest(BaseModel):
    url: str


class URLresponse(BaseModel):
    id: int
    original_url: str
    short_url: str
