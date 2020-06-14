"""
Entry point for the PSA Prizes package.
This module imports all functions to make them easily callable for the end user.
"""

from hypermodern_screening.psa_scrape import *


# Automate package version update.
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"