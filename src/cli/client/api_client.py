import requests

from src.cli.core.settings import get_settings

settings = get_settings()


def _extract_detail_message(detail: object) -> str | None:
    if isinstance(detail, list):
        parts: list[str] = []
        for item in detail:
            if isinstance(item, dict):
                msg = item.get("msg")
                parts.append(str(msg or item))
            else:
                parts.append(str(item))
        return "; ".join(parts) if parts else None

    if isinstance(detail, dict):
        msg = detail.get("msg")
        if msg:
            return str(msg)

    return None


def _extract_error_message(response: requests.Response) -> tuple[str, str | None]:
    try:
        payload = response.json()
    except ValueError:
        return (response.text or f"Erro HTTP {response.status_code}"), None

    code = None
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict):
            code = error.get("code")
            message = error.get("message")
            details = error.get("details")
            detail_message = _extract_detail_message(details)

            if (
                message
                and detail_message
                and message.lower().startswith("erro de valida")
            ):
                return detail_message, code
            if message:
                return str(message), code
            if detail_message:
                return detail_message, code

    return f"Erro HTTP {response.status_code}", code


def shorten_url(url: str) -> dict:
    shorten_endpoint = f"{settings.base_url}/shorten"
    data = {"url": url}
    response = requests.post(shorten_endpoint, json=data)

    if not response.ok:
        message, code = _extract_error_message(response)
        if code in ("URL_INVALIDA", "URL_INVALIDA"):
            raise ValueError(f"URL inválida: {message}")
        raise Exception(f"Erro na API {message}")

    return response.json()
