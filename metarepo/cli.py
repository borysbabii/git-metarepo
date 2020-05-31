"""Command line interface"""
import click

from .commands.list_cmd import list_repos
from .commands.status_cmd import status
from .commands.sync_cmd import sync


@click.group()
def cli():
    """Metarepo is a tool to help you to keep multiple git repositories in sync and organized"""


# Register commands
cli.add_command(status)
cli.add_command(list_repos)
cli.add_command(sync)

if __name__ == "__main__":
    cli()  # pragma: no cover