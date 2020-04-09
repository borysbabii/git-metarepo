"""List repositories command"""
import click
from multirepo import ui
from multirepo.cli_decorators import require_manifest


@click.command(name="list")
@require_manifest
def list_repos(manifest, _):
    """List all configured meta repositories"""
    repos = manifest.get_repos()

    ui.info(f"Listing {len(repos)} configured repositories")

    for repo in manifest.get_repos():
        ui.item(f"{repo.path}", ("uri", repo.uri))
