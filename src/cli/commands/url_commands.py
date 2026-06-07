from typing import Annotated

import pyperclip
import typer

from src.cli.client.api_client import get_url_stats, get_urls, shorten_url
from src.cli.ui.display import (
    display_error,
    display_stats,
    display_success,
    display_urls,
    show_loading,
)

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


@url_app.command("stats", help="Exibe as estatísticas de uma URL encurtada")
def stats(short_id: Annotated[str, typer.Argument(help="O ID curto da URL")]):
    try:
        with show_loading("Obtendo estatísticas..."):
            stats = get_url_stats(short_id)
        display_stats(stats)
    except ValueError as e:
        display_error(f"Erro de validação: {str(e)}")
    except Exception as e:
        display_error(f"Não foi possível obter as estatísticas: {str(e)}")


@url_app.command("list", help="Exibe todas as URLs encurtadas")
def list():
    try:
        with show_loading("Obtendo URLs..."):
            urls = get_urls()
        display_urls(urls)
    except Exception as e:
        display_error(f"Não foi possível obter as URLs: {str(e)}")
