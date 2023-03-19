"""Command-line interface."""

from typing import List
from typing import Optional

import click

from footie_fixtures import api


@click.group()
@click.version_option()
def cli() -> None:
    """Footie Fixtures."""


@cli.command(name="add_fixtures")
@click.option("-i", "--invite", "invites", multiple=True)
@click.option("-s", "--season")
@click.option("-d", "--dry-run", is_flag=True)
def add_fixtures(dry_run: bool, season: str, invites: Optional[List[str]]) -> None:
    """Add fixtures.

    Args:
        dry_run: whether it's a dry run or not
        season: the season for the fixtures
        invites: a list of email invites
    """
    click.echo("adding fixtures")
    api.add_fixtures(season=season, invites=invites)


@cli.command(name="delete_fixtures")
@click.option("-s", "--season")
@click.option("-d", "--dry-run", is_flag=True)
def delete_fixtures(dry_run: bool, season: str) -> None:
    """Delete fixtures.

    Args:
        dry_run: whether it's a dry run or not
        season: the season for the fixtures
    """
    click.echo("deleting fixtures")
    api.delete_fixtures()


@cli.command(name="add_invites")
@click.option("-i", "--invite", "invites", multiple=True, required=True)
@click.option("-d", "--dry-run", is_flag=True)
def add_invites(
    dry_run: bool,
    invites: List[str],
) -> None:
    """Add invites to upcoming existing events.

    Args:
        dry_run: whether it's a dry run or not
        invites: a list of email invites
    """
    click.echo("adding invites")
    api.add_invites(invites)


if __name__ == "__main__":
    cli(prog_name="footie-fixtures")  # pragma: no cover
