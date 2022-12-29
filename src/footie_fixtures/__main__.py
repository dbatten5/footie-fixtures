"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Footie Fixtures."""


if __name__ == "__main__":
    main(prog_name="footie-fixtures")  # pragma: no cover
