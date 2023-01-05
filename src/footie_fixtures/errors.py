"""Module to define custom errors."""


class NoRoundsError(Exception):
    """Raised when no rounds are available for the given season."""


class NoEventsError(Exception):
    """Raised when there are no events to delete."""
