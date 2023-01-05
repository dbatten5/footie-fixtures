"""Calendar utils."""

import os.path
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource
from googleapiclient.discovery import build

from .errors import NoEventsError


_SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar",
]


def build_service() -> Resource:
    """Build a Google Calendar service.

    Goes through authentication steps if necessary

    Returns:
        A googleapiclient.discovery.Resource object
    """
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", _SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                _SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def add_event(
    summary: str,
    description: str,
    start: str,
    attendees: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Add an event to the calendar.

    Args:
        summary: event summary
        description: event description
        start: event start time
        attendees: an optional list of attendees

    Returns:
        the returned event object
    """
    service = build_service()
    attendees = attendees or []

    start_dt = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S+00:00")
    end = (start_dt + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    payload = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start,
        },
        "end": {"dateTime": end},
        "attendees": [{"email": invite} for invite in attendees],
        "guestsCanInviteOthers": True,
        "extendedProperties": {
            "private": {
                "footie-fixtures": True,
            }
        },
    }

    event: Dict[str, Any] = (
        service.events()
        .insert(
            calendarId="primary",
            body=payload,
            sendUpdates="all",
        )
        .execute()
    )

    return event


def delete_footie_events() -> None:
    """Delete footie fixture events.

    Raises:
        NoEventsError: when there are no events to delete
    """
    service = build_service()

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            privateExtendedProperty="footie-fixtures=true",
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
        raise NoEventsError("No events to delete")

    for event in events:
        service.events().delete(
            calendarId="primary",
            eventId=event["id"],
        ).execute()
