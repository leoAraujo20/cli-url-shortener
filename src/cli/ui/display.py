from contextlib import contextmanager

from rich.console import Console

console = Console()


@contextmanager
def show_loading(message: str):
    with console.status(message, spinner="dots"):
        yield


def display_message(message: str, style: str = "bold green"):
    console.print(message, style=style)


def display_error(message: str):
    console.print(message, style="bold red")
