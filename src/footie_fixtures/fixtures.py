"""Fixtures."""

import datetime
from os import getenv
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import requests


FOOTBALL_API_KEY = getenv("FOOTBALL_API_KEY", "")
DEFAULT_LEAGUE_ID = "2"  # Champions League
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": FOOTBALL_API_KEY,
}


def get_rounds(
    league_id: Optional[Union[str, int]] = DEFAULT_LEAGUE_ID,
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
    payload = {"season": season, "league": DEFAULT_LEAGUE_ID}
    url = "https://v3.football.api-sports.io/fixtures/rounds"
    rounds: List[str] = requests.get(url, headers=HEADERS, params=payload).json()[
        "response"
    ]
    return rounds


def get_fixtures(
    league_id: Optional[str] = DEFAULT_LEAGUE_ID,
    season: Optional[str] = None,
    round: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a list of fixtures.

    Args:
        league_id: an optional league id
        season: an optional season, defaults to current year
        round: an optional round, otherwise the latest round will be used

    Returns:
        a dict of fixtures keyed by datetime
    """
    season = season or datetime.date.today().strftime("%Y")
    round = round or get_rounds(league_id, season)[-1]

    payload = {"season": season, "league": DEFAULT_LEAGUE_ID, "round": round}
    url = "https://v3.football.api-sports.io/fixtures"
    fixtures = requests.get(url, headers=HEADERS, params=payload).json()["response"]

    data: Dict[str, Any] = {
        "league": {
            "name": fixtures[0]["league"]["name"],
            "round": fixtures[0]["league"]["round"],
        },
        "fixtures": {},
    }

    for fixture in fixtures:
        date = fixture["fixture"]["date"]
        home = fixture["teams"]["home"]["name"]
        away = fixture["teams"]["away"]["name"]
        fixture_str = f"{home} vs. {away}"
        if date in data:
            data["fixtures"][date].append(fixture_str)
        else:
            data["fixtures"][date] = [fixture_str]

    return data
