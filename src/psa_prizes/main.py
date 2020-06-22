"""Call the main functions. Used by `poetry` as main script."""

from psa_prizes.analyze import analyze
from psa_prizes.scrape import scrape


def main() -> None:
    """Run psa-prizes."""
    scrape()
    analyze()
