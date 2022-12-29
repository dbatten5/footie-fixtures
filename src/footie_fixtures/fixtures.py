"""Fixtures."""

from os import getenv
from typing import Any
from typing import Dict

import requests


FOOTBALL_API_KEY = getenv("FOOTBALL_API_KEY", "")
LEAGUE_ID = "2"
SEASON = "2022"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": FOOTBALL_API_KEY,
}


def get_fixtures() -> Dict[str, Any]:
    """Get a list of fixtures.

    Returns:
        a dict of fixtures keyed by datetime
    """
    payload = {"season": SEASON, "league": LEAGUE_ID, "round": "Round of 16"}
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
