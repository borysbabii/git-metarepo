"""Checkout command"""
import click
from metarepo import ui, vcs_git
from metarepo.cli_decorators import require_manifest
from metarepo.manifest import Manifest


@click.command()
@click.option(
    "-b", "--branch", required=True, help="Create a new branch named <new_branch> and start it at <start_point>; see git-branch(1) for details"
)
@click.option(
    "-i", "--include", multiple=True, help="Include these projects."
)
@click.option(
    "-e", "--exclude", multiple=True, help="Exclude these projects."
)
@require_manifest
def checkout(manifest: Manifest, root_path: str, branch: str, include: list, exclude: list):
    """Switch branches or restore working tree files."""
    all_repos = manifest.get_repos()
    if include:
        repos = [repo for repo in all_repos if str(repo.path) in include]
    elif exclude:
        repos = [repo for repo in all_repos if str(repo.path) not in exclude]
    else:
        repos = all_repos

    ui.info(f"Checking out on branch {branch} for {len(repos)} repositories")

    for repo_data in repos:
        repo = vcs_git.RepoTool(root_path / repo_data.path, repo_data.url)
        repo.checkout('HEAD', branch)
        repo_status = repo.get_status()
        current_head = repo_status.active_branch.name if repo_status.active_branch else repo_status.head.hexsha[0:8]
        ui.item_ok(str(repo_data.path), ("track", repo_data.track), ("head", current_head), ("dirty", repo_status.is_dirty))
