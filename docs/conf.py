"""Sphinx configuration."""
from datetime import datetime


project = "PSA Prizes"
author = "Tobias Stenzel"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
html_static_path = ["_static"]

# Silence duplication error from citations that have the same reference.
exclude_patterns = ["references"]
