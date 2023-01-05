"""Tests for footie_fixtures.fixtures."""

import pytest

from footie_fixtures.errors import NoRoundsError
from footie_fixtures.fixtures import get_fixtures
from footie_fixtures.fixtures import get_rounds
from tests.conftest import my_vcr


class TestGetRounds:
    """Tests for the `get_rounds` function."""

    @my_vcr.use_cassette("fixtures/get_rounds.yaml")
    def test_success(self) -> None:
        """Test success."""
        rounds = get_rounds("2", "2022")
        assert rounds[-1] == "Round of 16"

    @my_vcr.use_cassette("fixtures/get_rounds_no_params.yaml")
    def test_no_params(self) -> None:
        """Test default params used."""
        rounds = get_rounds()
        assert len(rounds) == 0

    def test_headers(self) -> None:
        """Test correct headers added to request."""
        with my_vcr.use_cassette("fixtures/get_rounds.yaml") as cass:
            get_rounds("2", "2022")
            assert len(cass.requests) == 1
            req_headers = cass.requests[0].headers
            assert "x-rapidapi-key" in req_headers
            assert req_headers["x-rapidapi-host"] == "v3.football.api-sports.io"


class TestGetFixtures:
    """Tests for the `get_fixtures` function."""

    @my_vcr.use_cassette("fixtures/get_fixtures.yaml")
    def test_success(self) -> None:
        """Test success."""
        fixtures = get_fixtures("2", "2022", "Round of 16")
        assert fixtures["league"]["round"] == "Round of 16"
        assert fixtures["fixtures"]["2023-02-14T20:00:00+00:00"] == [
            "AC Milan vs. Tottenham",
            "Paris Saint Germain vs. Bayern Munich",
        ]

    def test_no_round(self) -> None:
        """Test default round param used."""
        with my_vcr.use_cassette("fixtures/get_fixtures_no_round.yaml") as cass:
            fixtures = get_fixtures(season="2022")
            assert len(cass.requests) == 2
            assert fixtures["league"]["round"] == "Round of 16"

    @my_vcr.use_cassette("fixtures/get_fixtures_no_season.yaml")
    def test_no_season(self) -> None:
        """Test default season param used."""
        fixtures = get_fixtures(round="Round of 16")
        assert fixtures["league"]["round"] == "Round of 16"

    @my_vcr.use_cassette("fixtures/get_fixtures_no_rounds.yaml")
    def test_no_rounds(self) -> None:
        """Test when no round data available."""
        with pytest.raises(NoRoundsError) as exc:
            get_fixtures()
            assert str(exc.value) == "No rounds available for season 2023"

    def test_headers(self) -> None:
        """Test correct headers added to request."""
        with my_vcr.use_cassette("fixtures/get_fixtures.yaml") as cass:
            get_fixtures("2", "2022", "Round of 16")
            assert len(cass.requests) == 1
            req_headers = cass.requests[0].headers
            assert "x-rapidapi-key" in req_headers
            assert req_headers["x-rapidapi-host"] == "v3.football.api-sports.io"
