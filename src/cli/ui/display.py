from contextlib import contextmanager

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

console = Console()


@contextmanager
def show_loading(message: str):
    with console.status(
        f"[bold #61afef]{message}[/]",
        spinner="bouncingBar",
        spinner_style="bold #c678dd",
    ):
        yield


def display_success(original_url: str, short_url: str, custom_message: str):
    mensagem = (
        f"[bold #61afef]{custom_message}[/]\n\n"
        f"[bold white]Original:[/]\n{original_url}\n\n"
        f"[bold #e5c07b]Encurtada:[/]\n[link={short_url}][bold #98c379]{short_url}[/][/link]\n\n"
        f"[italic dim]Copiado para a área de transferência![/]"
    )

    painel = Panel(
        Align.center(mensagem),
        title="[bold #98c379]Sucesso[/]",
        border_style="#98c379",
        padding=(1, 2),
        expand=False,
    )

    console.print()
    console.print(painel)
    console.print()


def display_error(message: str):
    painel = Panel(
        f"[bold #e06c75]{message}[/]",
        title="[bold #e06c75]Erro no Sistema[/]",
        border_style="#e06c75",
        padding=(1, 2),
        expand=False,
    )

    console.print()
    console.print(painel)
    console.print()
