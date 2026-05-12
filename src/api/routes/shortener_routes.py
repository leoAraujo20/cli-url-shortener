from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import select

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
    statement = select(URL).where(URL.original_url == request.url)
    db_url = session.exec(statement).first()

    if not db_url:
        db_url = URL(original_url=request.url)
        session.add(db_url)
        try:
            session.commit()
            session.refresh(db_url)
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar URL: no banco de dados {str(e)}",
            )
    short_id = encode_base62(db_url.id)
    short_url = f"{settings.base_url}/{short_id}"
    return URLresponse(short_url=short_url)


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
