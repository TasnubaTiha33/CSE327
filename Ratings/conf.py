# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BookVault'
copyright = '2024, Tasnuba Islam'
author = 'Tasnuba Islam'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
import os
import sys
sys.path.insert(0, os.path.abspath('../app'))  # Adjust the path as per your directory structure
# extensions
extensions = [
    'sphinx.ext.autodoc',
    # Add other extensions like 'sphinx.ext.napoleon' for Google-style docstrings, etc.
]

# If you want to include private members too, you can do this:
autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']

# If you want to exclude certain modules, you can add them here
# exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
