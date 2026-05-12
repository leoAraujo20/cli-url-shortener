import time
from typing import Annotated

import pyperclip
import typer

from src.cli.client.api_client import shorten_url
from src.cli.ui.display import display_error, display_success, show_loading

url_app = typer.Typer(help="Comandos relacionados a URLs")


@url_app.command("shorten", help="Encurta uma URL e copia para a área de transferência")
def shorten(url: Annotated[str, typer.Argument(help="The URL to shorten")]):
    try:
        with show_loading("Encurtando a URL..."):
            time.sleep(5)
            shortened_url = shorten_url(url)
        pyperclip.copy(shortened_url)
        display_success(url, shortened_url)
    except Exception as e:
        display_error(f"Não foi possível encurtar a URL: {str(e)}")
