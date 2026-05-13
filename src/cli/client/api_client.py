import requests

from src.cli.core.settings import get_settings

settings = get_settings()


def shorten_url(url: str) -> dict:
    shorten_endpoint = f"{settings.base_url}/shorten"
    data = {"url": url}
    response = requests.post(shorten_endpoint, json=data)

    if not response.ok:
        error_json = response.json()
        error_message = error_json.get("detail", "Unknown error")
        raise Exception(f"API error: {error_message}")

    return response.json()
