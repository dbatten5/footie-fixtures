"""Football api."""

import datetime
from os import getenv
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import requests

from .errors import NoRoundsError


FOOTBALL_API_KEY = getenv("FOOTBALL_API_KEY", "")
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": FOOTBALL_API_KEY,
}


def get_rounds(
    league_id: Union[str, int],
    season: Optional[Union[str, int]] = None,
) -> List[str]:
    """Get a list of the upcoming rounds for a league.

    Args:
        league_id: an optional league id
        season: an optional season, defaults to current year

    Returns:
        a list of rounds
    """
    season = season or datetime.date.today().strftime("%Y")
    payload = {"season": season, "league": league_id}
    url = "https://v3.football.api-sports.io/fixtures/rounds"
    rounds: List[str] = requests.get(url, headers=HEADERS, params=payload).json()[
        "response"
    ]
    return rounds


def get_fixtures(
    league_id: Union[str, int],
    season: Optional[str] = None,
    round: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a list of fixtures.

    Args:
        league_id: an optional league id
        season: an optional season, defaults to current year
        round: an optional round, otherwise the latest round will be used

    Raises:
        NoRoundsError: when there are no rounds available for the season

    Returns:
        a dict of fixtures keyed by datetime
    """
    season = season or datetime.date.today().strftime("%Y")
    if not round:
        rounds = get_rounds(league_id, season)
        if not rounds:
            raise NoRoundsError(f"No rounds available for season {season}")
        round = rounds[-1]

    payload = {"season": season, "league": league_id, "round": round}
    url = "https://v3.football.api-sports.io/fixtures"
    fixtures = requests.get(url, headers=HEADERS, params=payload).json()["response"]

    data: Dict[str, Any] = {
        "league": {
            "name": "",
            "round": round,
        },
        "fixtures": {},
    }

    if not fixtures:
        return data

    data["league"] = {
        "name": fixtures[0]["league"]["name"],
        "round": fixtures[0]["league"]["round"],
    }

    for fixture in fixtures:
        date = fixture["fixture"]["date"]
        home = fixture["teams"]["home"]["name"]
        away = fixture["teams"]["away"]["name"]
        fixture_str = f"{home} vs. {away}"
        if date in data["fixtures"]:
            data["fixtures"][date].append(fixture_str)
        else:
            data["fixtures"][date] = [fixture_str]

    return data
