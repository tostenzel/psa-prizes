"""Call the main functions. Used by poetry a main script."""

from psa_prizes.scrape import parse_scrape_store
from psa_prizes.analyze import analyze


def main() -> None:
    """Run psa-prizes."""
    parse_scrape_store()
    analyze()
