import requests

from src.cli.core.settings import get_settings

settings = get_settings()


def _normalize_url(url: str) -> str:
    cleaned = url.strip().strip('"').strip("'")
    cleaned = cleaned.replace("\\/", "/")

    if not cleaned:
        raise ValueError("A URL não pode ser vazia")
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned

    return cleaned


def _extract_error_message(response: requests.Response) -> tuple[str, str | None]:
    try:
        payload = response.json()
    except ValueError:
        return (response.text or f"Erro HTTP {response.status_code}"), None

    error_data = payload.get("error", {})
    code = error_data.get("code")
    message = error_data.get("message", f"Erro HTTP {response.status_code}")
    details = error_data.get("details")

    if code == "ERROS_DE_VALIDACAO" and isinstance(details, list):
        validation_errors = "\n".join(
            [f"- {err.get('loc', [''])[-1]}: {err.get('msg', '')}" for err in details]
        )
        message = f"Erros de validação: \n{validation_errors}"

    return message, code


def shorten_url(url: str) -> dict:
    url = _normalize_url(url)
    shorten_endpoint = f"{settings.base_url}/shorten"
    data = {"url": url}
    try:
        response = requests.post(shorten_endpoint, json=data, timeout=10)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro de conexão com a API: {e}")

    if not response.ok:
        message, code = _extract_error_message(response)
        if code in ("URL_INVALIDA", "ERROS_DE_VALIDACAO"):
            raise ValueError(f"URL inválida: {message}")
        raise Exception(f"Erro na API {message}")

    return response.json()


def get_url_stats(short_id: str) -> dict:
    stats_endpoint = f"{settings.base_url}/stats/{short_id}"
    try:
        response = requests.get(stats_endpoint, timeout=10)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro de conexão com a API: {e}")

    if not response.ok:
        message, code = _extract_error_message(response)
        if code == "URL_CURTA_INVALIDA":
            raise ValueError(f"ID curto inválido: {message}")
        raise Exception(f"Erro na API: {message}")

    return response.json()
