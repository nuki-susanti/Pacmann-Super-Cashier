import typer
from rich.table import Table
from rich.console import Console


console = Console()

def typer_style(message, color_font=None):

    if color_font:
        fg = typer.colors.RED
    else:
        fg = typer.colors.GREEN

    return typer.echo(typer.style(f'{message}', bg=typer.colors.WHITE, fg=fg))

def pretty_table(data, headers=None):
    
    if headers:
        headers = ['No', 'Nama Item', 'Harga per Item (Rp.)']
    else:
        headers = ['No', 'Nama Item', 'Harga per Item (Rp.)', 'Jumlah Item', 'Harga Total (Rp.)']
    table = Table(*headers, show_header=True, header_style=f'bold green')

    for row in data:
        table.add_row(*map(str, row))

    console.print(table)