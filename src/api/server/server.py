from fastapi import FastAPI

from src.api.routes.shortener_routes import shortener_router

app = FastAPI()

app.include_router(shortener_router)
