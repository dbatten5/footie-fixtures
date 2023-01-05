"""Tests for footie_fixtures.calendar_utils."""

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from footie_fixtures.calendar_utils import add_event
from footie_fixtures.calendar_utils import build_service
from footie_fixtures.calendar_utils import delete_footie_events
from footie_fixtures.errors import NoEventsError


MODULE_PATH = "footie_fixtures.calendar_utils"


class TestBuildService:
    """Tests for the `build_service` function."""

    @patch(f"{MODULE_PATH}.build")
    @patch(f"{MODULE_PATH}.Credentials")
    @patch(f"{MODULE_PATH}.os.path.exists")
    def test_creds_present(
        self,
        mock_os_path_exists: MagicMock,
        mock_credentials: MagicMock,
        mock_build: MagicMock,
    ) -> None:
        """Test when credentials are already present."""
        mock_os_path_exists.return_value = True
        mock_creds = mock_credentials.from_authorized_user_file.return_value

        service = build_service()

        assert service == mock_build.return_value
        mock_os_path_exists.assert_called_once_with("token.json")
        mock_credentials.from_authorized_user_file.assert_called_once_with(
            "token.json",
            [
                "https://www.googleapis.com/auth/calendar.events",
                "https://www.googleapis.com/auth/calendar",
            ],
        )
        mock_build.assert_called_once_with("calendar", "v3", credentials=mock_creds)

    @patch(f"{MODULE_PATH}.build")
    @patch(f"{MODULE_PATH}.InstalledAppFlow")
    @patch(f"{MODULE_PATH}.os.path.exists")
    def test_creds_not_present(
        self,
        mock_os_path_exists: MagicMock,
        mock_app_flow: MagicMock,
        mock_build: MagicMock,
    ) -> None:
        """Test when credentials are not present."""
        mock_os_path_exists.return_value = False
        mock_flow = mock_app_flow.from_client_secrets_file.return_value
        mock_creds = mock_flow.run_local_server.return_value

        with patch("builtins.open", mock_open()) as m:
            service = build_service()

        assert service == mock_build.return_value
        mock_build.assert_called_once_with("calendar", "v3", credentials=mock_creds)
        mock_app_flow.from_client_secrets_file.assert_called_once_with(
            "credentials.json",
            [
                "https://www.googleapis.com/auth/calendar.events",
                "https://www.googleapis.com/auth/calendar",
            ],
        )
        mock_flow.run_local_server.assert_called_once_with(port=0)
        handle = m()
        handle.write.assert_called_once_with(mock_creds.to_json.return_value)

    @patch(f"{MODULE_PATH}.build")
    @patch(f"{MODULE_PATH}.Request")
    @patch(f"{MODULE_PATH}.Credentials")
    @patch(f"{MODULE_PATH}.os.path.exists")
    def test_creds_not_valid(
        self,
        mock_os_path_exists: MagicMock,
        mock_credentials: MagicMock,
        mock_request: MagicMock,
        mock_build: MagicMock,
    ) -> None:
        """Test when credentials are present but not valid."""
        mock_os_path_exists.return_value = True
        mock_creds = Mock(valid=False, expired=True, refresh_token=True)
        mock_credentials.from_authorized_user_file.return_value = mock_creds

        with patch("builtins.open", mock_open()) as m:
            service = build_service()

        assert service == mock_build.return_value
        mock_creds.refresh.assert_called_once_with(mock_request.return_value)
        mock_build.assert_called_once_with("calendar", "v3", credentials=mock_creds)
        handle = m()
        handle.write.assert_called_once_with(mock_creds.to_json.return_value)


class TestAddEvent:
    """Tests for the `add_event` function."""

    @patch(f"{MODULE_PATH}.build_service")
    def test_success(self, mock_build_service: MagicMock) -> None:
        """Test success."""
        mock_service = Mock()
        mock_build_service.return_value = mock_service

        summary = "Event summary"
        description = "Event description"
        start = "2022-01-01T20:00:00+00:00"
        attendees = ["a@b.com", "c@d.com"]

        event = add_event(
            summary=summary, description=description, start=start, attendees=attendees
        )

        payload = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start,
            },
            "end": {"dateTime": "2022-01-01T22:00:00+00:00"},
            "attendees": [{"email": "a@b.com"}, {"email": "c@d.com"}],
            "guestsCanInviteOthers": True,
            "extendedProperties": {
                "private": {
                    "footie-fixtures": True,
                }
            },
        }

        assert (
            event
            == mock_service.events.return_value.insert.return_value.execute.return_value
        )
        mock_events = mock_service.events.return_value
        mock_events.insert.assert_called_once_with(
            calendarId="primary",
            body=payload,
            sendUpdates="all",
        )


class TestDeleteFootieEvents:
    """Tests for the `delete_footie_events` function."""

    @patch(f"{MODULE_PATH}.build_service")
    def test_success(self, mock_build_service: MagicMock) -> None:
        """Test success."""
        mock_service = Mock()
        mock_build_service.return_value = mock_service
        mock_service.events.return_value.list.return_value.execute.return_value = {
            "items": [{"id": 1}, {"id": 2}]
        }

        delete_footie_events()

        mock_events = mock_service.events.return_value
        mock_events.list.assert_called_once_with(
            calendarId="primary",
            privateExtendedProperty="footie-fixtures=true",
        )
        mock_events.delete.assert_has_calls(
            [
                call(calendarId="primary", eventId=1),
                call().execute(),
                call(calendarId="primary", eventId=2),
                call().execute(),
            ]
        )

    @patch(f"{MODULE_PATH}.build_service")
    def test_no_events(self, mock_build_service: MagicMock) -> None:
        """Test for when there are no events to delete."""
        mock_service = Mock()
        mock_build_service.return_value = mock_service
        mock_service.events.return_value.list.return_value.execute.return_value = {
            "items": []
        }

        with pytest.raises(NoEventsError):
            delete_footie_events()
