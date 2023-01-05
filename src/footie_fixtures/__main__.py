"""Command-line interface."""

from typing import List
from typing import Optional

import click

from footie_fixtures import add_fixtures as api_add_fixtures
from footie_fixtures.api import DEFAULT_LEAGUE_ID
from footie_fixtures.football_api import get_fixtures


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
    if dry_run:
        fixtures = get_fixtures(
            DEFAULT_LEAGUE_ID,
            season=season,
        )
        click.echo(
            f"dry run enabled - skipped adding {len(fixtures['fixtures'])} events"
        )
        click.echo(
            f"league: {fixtures['league']['name']}, round: {fixtures['league']['round']}"
        )
    else:
        click.echo("adding fixtures")
        api_add_fixtures(season=season, invites=invites)


if __name__ == "__main__":
    cli(prog_name="footie-fixtures")  # pragma: no cover
