from typing import Annotated

import pyperclip
import typer

from src.cli.client.api_client import shorten_url
from src.cli.ui.display import display_error, display_success, show_loading

url_app = typer.Typer(help="Comandos relacionados a URLs")


@url_app.command("shorten", help="Encurta uma URL e copia para a área de transferência")
def shorten(url: Annotated[str, typer.Argument(help="A URL que você deseja encurtar")]):
    try:
        with show_loading("Encurtando a URL..."):
            response = shorten_url(url)
        pyperclip.copy(response["short_url"])
        display_success(
            original_url=response["original_url"],
            short_url=response["short_url"],
            custom_message=response["message"],
        )
    except ValueError as e:
        display_error(f"Erro de validação: {str(e)}")
    except Exception as e:
        display_error(f"Não foi possível encurtar a URL: {str(e)}")
