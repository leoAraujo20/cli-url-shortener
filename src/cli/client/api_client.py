import requests

from src.cli.core.settings import get_settings

settings = get_settings()


def shorten_url(url: str) -> str:
    shorten_endpoint = f"{settings.base_url}/shorten"
    data = {"url": url}
    response = requests.post(shorten_endpoint, json=data)
    return response.json()["short_url"]
