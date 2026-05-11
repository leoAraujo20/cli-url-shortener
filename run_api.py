import uvicorn

from src.api.core.settings import get_settings

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        "src.api.server.server:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
