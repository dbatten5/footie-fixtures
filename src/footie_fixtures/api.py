"""Public api."""

from typing import List
from typing import Optional
from typing import Union

from .calendar_utils import add_event
from .errors import NoFixturesError
from .football_api import get_fixtures


DEFAULT_LEAGUE_ID = "2"  # Champions League


def add_fixtures(
    league_id: Union[str, int] = DEFAULT_LEAGUE_ID,
    season: Optional[str] = None,
    round: Optional[str] = None,
    invites: Optional[List[str]] = None,
    dry_run: bool = False,
) -> None:
    """Add fixtures to the calendar.

    Args:
        league_id: a league id
        season: a season, defaults to current year
        round: an optional round, otherwise the latest round will be used
        invites: a list of email address to add to the invite list
        dry_run: a flag to determine whether the events should be added

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

    for date, teams in fixtures["fixtures"].items():
        add_event(
            summary=f"{league_name}: {fixtures['league']['round']}",
            description="\n".join(teams),
            start=date,
            attendees=invites,
        )
