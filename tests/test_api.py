"""Tests for the main api."""

from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

import pytest

from footie_fixtures.api import DEFAULT_LEAGUE_ID
from footie_fixtures.api import add_fixtures
from footie_fixtures.errors import NoFixturesError


MODULE_PATH = "footie_fixtures.api"


class TestAddFixtures:
    """Tests for the `add_fixtures` function."""

    @patch(f"{MODULE_PATH}.get_fixtures")
    def test_no_fixtures(self, mock_get_fixtures: MagicMock) -> None:
        """Test no fixtures returned."""
        mock_get_fixtures.return_value = {"fixtures": {}}

        with pytest.raises(NoFixturesError):
            add_fixtures(season="2022", round="Up")

        mock_get_fixtures.assert_called_once_with(
            league_id=DEFAULT_LEAGUE_ID, season="2022", round="Up"
        )

    @patch(f"{MODULE_PATH}.add_event")
    @patch(f"{MODULE_PATH}.get_fixtures")
    def test_success(
        self,
        mock_get_fixtures: MagicMock,
        mock_add_event: MagicMock,
    ) -> None:
        """Test success."""
        mock_get_fixtures.return_value = {
            "league": {"name": "foo", "round": "bar"},
            "fixtures": {
                "tomorrow": ["me vs you", "they vs them"],
                "day after": ["bill vs bob", "jen vs jill"],
            },
        }

        add_fixtures(season="2022", round="Up", invites=["a@b.com"])

        mock_add_event.assert_has_calls(
            [
                call(
                    summary="foo: bar",
                    description="me vs you\nthey vs them",
                    start="tomorrow",
                    attendees=["a@b.com"],
                ),
                call(
                    summary="foo: bar",
                    description="bill vs bob\njen vs jill",
                    start="day after",
                    attendees=["a@b.com"],
                ),
            ]
        )
