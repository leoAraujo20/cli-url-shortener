from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import col, func, select

from src.api.core.base62 import decode_base62, encode_base62
from src.api.core.database import get_session
from src.api.core.exceptions import URLNotFoundException
from src.api.core.settings import get_settings
from src.api.models.shortener_models import URL, URLAccess
from src.api.schemas.shortener_schemas import (
    ShortenResponse,
    URLrequest,
    URLResponse,
    URLStatsResponse,
)

shortener_router = APIRouter(prefix="/api", tags=["Shortener"])
settings = get_settings()


@shortener_router.post(
    "/shorten", response_model=ShortenResponse, status_code=HTTPStatus.CREATED
)
def shorten_original_url(
    request: URLrequest, response: Response, session=Depends(get_session)
):
    statement = select(URL).where(URL.original_url == request.url)
    db_url = session.exec(statement).first()
    response_message = ""

    if not db_url:
        db_url = URL(original_url=request.url)
        session.add(db_url)
        try:
            session.commit()
            session.refresh(db_url)
            response_message = "URL encurtada com sucesso!"
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar URL: no banco de dados {str(e)}",
            )
    else:
        response.status_code = HTTPStatus.OK
        response_message = "URL já encurtada anteriormente."

    short_id = encode_base62(db_url.id)
    short_url = f"{settings.base_url}/{short_id}"
    return ShortenResponse(
        id=db_url.id,
        original_url=db_url.original_url,
        short_url=short_url,
        message=response_message,
    )


@shortener_router.get(
    "/stats/{short_id}", status_code=HTTPStatus.OK, response_model=URLStatsResponse
)
def get_url_stats(short_id: str, session=Depends(get_session)):
    try:
        url_id = decode_base62(short_id)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="URL curta inválida"
        )

    db_url = session.get(URL, url_id)
    if not db_url:
        raise URLNotFoundException(short_id=short_id)

    statement = select(func.count(col(URLAccess.id))).where(URLAccess.url_id == url_id)
    total_accesses = session.exec(statement).one()

    short_url = f"{settings.base_url}/{short_id}"

    if total_accesses == 0:
        return URLStatsResponse(
            original_url=db_url.original_url,
            short_url=short_url,
            total_accesses=0,
            top_referrers={},
            unique_visitors=0,
            recent_accesses=[],
        )

    statement = select(func.count(func.distinct(URLAccess.ip_address))).where(
        URLAccess.url_id == url_id
    )
    unique_visitors = session.exec(statement).one()

    statement = (
        select(URLAccess.referrer, func.count(col(URLAccess.id)))
        .where(URLAccess.url_id == url_id)
        .group_by(URLAccess.referrer)
        .order_by(func.count(col(URLAccess.id)).desc())
    )

    referrers_data = session.exec(statement).all()
    top_referrers = {
        (ref if ref else "Tráfego Direto"): count for ref, count in referrers_data
    }

    statement = (
        select(URLAccess)
        .where(URLAccess.url_id == url_id)
        .order_by(col(URLAccess.accessed_at).desc())
        .limit(5)
    )
    recent_accesses = session.exec(statement).all()

    return URLStatsResponse(
        original_url=db_url.original_url,
        short_url=short_url,
        total_accesses=total_accesses,
        top_referrers=top_referrers,
        unique_visitors=unique_visitors,
        recent_accesses=recent_accesses,
    )


@shortener_router.get(
    "/links",
    status_code=HTTPStatus.OK,
    response_model=list[URLResponse],
)
def get_urls(session=Depends(get_session)):
    statement = select(URL).limit(50)
    urls = session.exec(statement).all()

    urls_with_short_id = [
        {
            "id": url.id,
            "original_url": url.original_url,
            "short_url": f"{settings.base_url}/{encode_base62(url.id)}",
        }
        for url in urls
    ]

    return urls_with_short_id
