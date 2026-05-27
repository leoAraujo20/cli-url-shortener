import requests

from src.cli.core.settings import get_settings

settings = get_settings()


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
    shorten_endpoint = f"{settings.base_url}/shorten"
    data = {"url": url}
    response = requests.post(shorten_endpoint, json=data)

    if not response.ok:
        message, code = _extract_error_message(response)
        if code in ("URL_INVALIDA", "ERROS_DE_VALIDACAO"):
            raise ValueError(f"URL inválida: {message}")
        raise Exception(f"Erro na API {message}")

    return response.json()
