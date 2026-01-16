"""Entry point for fapi-cli."""

from .cli import app


def main() -> None:
    """Run the CLI application."""

    app()


if __name__ == "__main__":  # pragma: no cover
    main()
