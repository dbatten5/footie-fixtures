"""Public api."""

from typing import List
from typing import Optional
from typing import Union

import click

from .calendar_utils import add_event
from .calendar_utils import delete_footie_events
from .calendar_utils import update_footie_events
from .errors import NoFixturesError
from .football_api import get_fixtures
from .utils import _dry_run_enabled


DEFAULT_LEAGUE_ID = "2"  # Champions League


def add_fixtures(
    league_id: Union[str, int] = DEFAULT_LEAGUE_ID,
    season: Optional[str] = None,
    round: Optional[str] = None,
    invites: Optional[List[str]] = None,
) -> None:
    """Add fixtures to the calendar.

    Args:
        league_id: a league id
        season: a season, defaults to current year
        round: an optional round, otherwise the latest round will be used
        invites: a list of email address to add to the invite list

    Raises:
        NoFixturesError: when there no fixtures to add
    """
    invites = invites or []

    fixtures = get_fixtures(
        league_id=league_id,
        season=season,
        round=round,
    )

    if not fixtures["fixtures"]:
        raise NoFixturesError

    league_name = fixtures["league"]["name"]

    if _dry_run_enabled():
        click.echo("dry run enabled")
        click.echo(f"skipped adding {len(fixtures['fixtures'])} events:")
        click.echo(
            f"league: {fixtures['league']['name']}, round: {fixtures['league']['round']}"
        )
        return

    for date, teams in fixtures["fixtures"].items():
        add_event(
            summary=f"{league_name}: {fixtures['league']['round']}",
            description="\n".join(teams),
            start=date,
            attendees=invites,
        )


def delete_fixtures() -> None:
    """Delete fixtures from the calendar."""
    delete_footie_events()


def add_invites(invites: List[str]) -> None:
    """Add new invites to existing events.

    Args:
        invites: a list of email address to add to the invite list
    """
    attendees = [{"email": invite} for invite in invites]

    update_footie_events({"attendees": attendees})
