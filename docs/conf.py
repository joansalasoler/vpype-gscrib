import sys
from pathlib import Path

sys.path.insert(0, str(Path('..').resolve()))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'vpype-mecode'
copyright = '2025, Joan Sala <contact@joansala.com>'
author = 'Joan Sala'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_click",
    "myst_parser",
]

root_doc = "index"
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv', 'mecode']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
modindex_common_prefix = ["vpype_mecode."]

# -- External Documentation Mappings -----------------------------------------

intersphinx_mapping = {
    "click": ("https://click.palletsprojects.com/en/7.x/", None),
    "python": ("https://docs.python.org/3/", None),
}
