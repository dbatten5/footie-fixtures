"""Tests for footie_fixtures.fixtures."""

from footie_fixtures.fixtures import HEADERS
from footie_fixtures.fixtures import get_rounds
from tests.conftest import my_vcr


class TestGetRounds:
    """Tests for the `get_rounds` method."""

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
            assert cass.requests[0].headers == HEADERS


class TestGetFixtures:
    """Tests for the `get_fixtures` method."""
