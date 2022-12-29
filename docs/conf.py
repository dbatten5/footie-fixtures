"""Sphinx configuration."""
project = "Footie Fixtures"
author = "Dom Batten"
copyright = "2022, Dom Batten"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
