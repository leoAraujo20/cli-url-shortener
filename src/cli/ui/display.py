from contextlib import contextmanager

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

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


def display_stats(stats: dict):
    stats_message = (
        f"[bold white]Original:[/]\n{stats['original_url']}\n\n"
        f"[bold #e5c07b]Encurtada:[/]\n[link={stats['short_url']}][bold #98c379]{stats['short_url']}[/][/link]\n\n"
        f"[bold #56b6c2]Cliques Totais:[/] {stats['total_accesses']}\n"
        f"[bold #56b6c2]Visitas únicas:[/] {stats['unique_visitors']}\n"
    )

    ref_table = Table(
        title="[bold #e5c07b]Top Origens[/]",
        show_header=True,
        header_style="bold #56b6c2",
        box=box.SIMPLE,
    )

    ref_table.add_column("Origem", style="white")
    ref_table.add_column("Cliques", justify="right", style="bold #98c379")

    referrers = stats.get("top_referrers", {})
    if referrers:
        for ref, clicks in referrers.items():
            ref_table.add_row(ref, str(clicks))
    else:
        ref_table.add_row("[dim]Nenhum clique ainda[/]", "-")

    acc_table = Table(
        title="\n[bold #e5c07b]Últimos Acessos[/]",
        show_header=True,
        header_style="bold #56b6c2",
        box=box.SIMPLE,
    )

    acc_table.add_column("Data/Hora", style="dim")
    acc_table.add_column("IP", style="blue")
    acc_table.add_column(
        "Dispositivo/Navegador", max_width=40, overflow="ellipsis", style="yellow"
    )

    accesses = stats.get("recent_accesses", [])
    if accesses:
        for acc in accesses:
            acc_table.add_row(
                acc["accessed_at"],
                acc["ip_address"] or "-",
                acc["user_agent"] or "-",
            )
    else:
        acc_table.add_row("[dim]Nenhum acesso registrado[/]", "-", "-")

    panel_content = Group(stats_message, ref_table, acc_table)

    panel = Panel(
        Align.left(panel_content),
        title="[bold #56b6c2]📊 Dashboard de Estatísticas[/]",
        border_style="#56b6c2",
        padding=(1, 2),
        expand=False,
    )

    console.print()
    console.print(panel)
    console.print()
