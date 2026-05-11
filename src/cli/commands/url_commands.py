from typing import Annotated

import pyperclip
import typer

from src.cli.client.api_client import shorten_url
from src.cli.ui.display import display_error, display_message, show_loading

url_app = typer.Typer(help="Comandos relacionados a URLs")


@url_app.command("shorten", help="Encurta uma URL e copia para a área de transferência")
def shorten(url: Annotated[str, typer.Argument(help="The URL to shorten")]):
    clear_url = url.replace("\\", "")
    try:
        with show_loading("Encurtando a URL..."):
            shortened_url = shorten_url(clear_url)
        pyperclip.copy(shortened_url)
        display_message(
            f"URL encurtada: {shortened_url}(copiada para a área de transferência)"
        )
    except Exception as e:
        display_error(f"Não foi possível encurtar a URL: {str(e)}")
