from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.core.exceptions import InvalidURLException, URLNotFoundException
from src.api.routes.shortener_routes import shortener_router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    for error in exc.errors():
        if "ctx" in error and "error" in error["ctx"]:
            current_error = error["ctx"]["error"]

            if isinstance(current_error, InvalidURLException):
                return JSONResponse(
                    status_code=422,
                    content={
                        "error": "URL_INVALIDA",
                        "message": current_error.message,
                        "url_recebida": current_error.url,
                    },
                )

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(URLNotFoundException)
async def url_not_found_exception_handler(request: Request, exc: URLNotFoundException):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={
            "error": "URL_NAO_ENCONTRADA",
            "message": exc.message,
            "short_id": exc.short_id,
        },
    )


app.include_router(shortener_router)
