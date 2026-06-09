from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.core.exceptions import InvalidURLException, URLNotFoundException
from src.api.routes.redirect_routes import redirect_router
from src.api.routes.shortener_routes import shortener_router

app = FastAPI()


def _error_payload(code: str, message: str, details: object | None = None) -> dict:
    error: dict[str, object] = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return {"error": error}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    for error in exc.errors():
        ctx = error.get("ctx", {})
        current_error = ctx.get("error")
        if isinstance(current_error, InvalidURLException):
            return JSONResponse(
                status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
                content=_error_payload(
                    code="URL_INVALIDA",
                    message=current_error.message,
                    details={"url": current_error.url},
                ),
            )

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        content=_error_payload(
            code="ERROS_DE_VALIDACAO",
            message="Erro de validação dos dados enviados",
            details=exc.errors(),
        ),
    )


@app.exception_handler(URLNotFoundException)
async def url_not_found_exception_handler(request: Request, exc: URLNotFoundException):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=_error_payload(
            code="URL_NAO_ENCONTRADA",
            message=exc.message,
            details={"short_id": exc.short_id},
        ),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if isinstance(exc.detail, str):
        message = exc.detail
        details = None
    else:
        message = "Erro HTTP"
        details = exc.detail
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(
            code="ERRO_HTTP",
            message=message,
            details=details,
        ),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=_error_payload(
            code="ERRO_INTERNO",
            message="Ocorreu um erro interno no servidor",
        ),
    )


app.include_router(shortener_router)
app.include_router(redirect_router)
