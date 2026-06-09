from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from src.api.core.base62 import decode_base62
from src.api.core.database import get_session
from src.api.core.exceptions import URLNotFoundException
from src.api.models.shortener_models import URL, URLAccess

redirect_router = APIRouter()


@redirect_router.get("/{short_id}", status_code=HTTPStatus.FOUND)
def redirect_to_original_url(
    short_id: str, request: Request, session=Depends(get_session)
):
    try:
        url_id = decode_base62(short_id)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="URL curta inválida"
        )

    db_url = session.get(URL, url_id)
    if not db_url:
        raise URLNotFoundException(short_id=short_id)

    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")
    ip_address = request.client.host if request.client else None

    access_record = URLAccess(
        url_id=url_id, user_agent=user_agent, referrer=referrer, ip_address=ip_address
    )
    session.add(access_record)
    session.commit()

    return RedirectResponse(db_url.original_url)
