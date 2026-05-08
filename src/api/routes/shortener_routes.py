from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from src.api.core.base62 import decode_base62, encode_base62
from src.api.core.database import get_session
from src.api.core.settings import get_settings
from src.api.models.shortener_models import URL
from src.api.schemas.shortener_schemas import URLrequest, URLresponse

shortener_router = APIRouter()
settings = get_settings()


@shortener_router.post(
    "/shorten", response_model=URLresponse, status_code=HTTPStatus.CREATED
)
def shorten_original_url(request: URLrequest, session=Depends(get_session)):
    db_url = URL(original_url=request.url)
    session.add(db_url)
    session.commit()
    session.refresh(db_url)

    short_url = f"{settings.base_url}/{encode_base62(db_url.id)}"

    return URLresponse(
        id=db_url.id, original_url=db_url.original_url, short_url=short_url
    )


@shortener_router.get("/{short_id}", status_code=HTTPStatus.FOUND)
def redirect_to_original_url(short_id: str, session=Depends(get_session)):
    try:
        url_id = decode_base62(short_id)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid short URL"
        )

    db_url = session.get(URL, url_id)
    if not db_url:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="URL not found")

    return RedirectResponse(db_url.original_url)
