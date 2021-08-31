"""Checkout command"""
import click
from metarepo import ui, vcs_git
from metarepo.cli_decorators import require_manifest
from metarepo.manifest import Manifest


@click.command()
@click.option(
    "-m", "--message", required=True, help="Use the given <msg> as the commit message"
)
@click.option(
    "-i", "--include", multiple=True, help="Include these projects."
)
@click.option(
    "-e", "--exclude", multiple=True, help="Exclude these projects."
)
@require_manifest
def commit(manifest: Manifest, root_path: str, message: str, include: list, exclude: list):
    """Record changes to the repository."""
    all_repos = manifest.get_repos()
    if include:
        repos = [repo for repo in all_repos if str(repo.path) in include]
    elif exclude:
        repos = [repo for repo in all_repos if str(repo.path) not in exclude]
    else:
        repos = all_repos

    ui.info(f"Storing change to {len(repos)} repositories")

    for repo_data in repos:
        repo = vcs_git.RepoTool(root_path / repo_data.path, repo_data.url)
        repo_status = repo.get_status()
        if repo_status.is_dirty:
            repo.commit(message)
            ui.item_ok(f'saved {str(repo_data.path)}')
        else:
            ui.item_error(str(repo_data.path), 'nothing to commit.')
