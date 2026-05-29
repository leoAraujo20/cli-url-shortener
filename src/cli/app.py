import typer

from src.cli.commands.url_commands import url_app

app = typer.Typer(help="Ferramenta de encurtamento de URLs")
app.add_typer(url_app)
