"""Utils module."""
import click


def _dry_run_enabled() -> bool:
    return bool(click.get_current_context().params["dry_run"])
