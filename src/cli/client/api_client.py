import requests

from src.cli.core.settings import get_settings

settings = get_settings()


def shorten_url(url: str) -> dict:
    shorten_endpoint = f"{settings.base_url}/shorten"
    data = {"url": url}
    response = requests.post(shorten_endpoint, json=data)

    if not response.ok:
        error_json = response.json()
        if error_json.get("error") == "URL_INVALIDA":
            message = error_json.get("message", "URL inválida")
            raise ValueError(message)
        else:
            detail = error_json.get("detail", "Erro desconhecido")
            if isinstance(detail, list):
                detail = "; ".join([f"{err['loc']}: {err['msg']}" for err in detail])
            raise ValueError(f"Erros de validação: {detail}")

    return response.json()
