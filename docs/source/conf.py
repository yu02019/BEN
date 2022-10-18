# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'BEN'
copyright = '2022, Ziqi Yu'
author = 'Ziqi Yu'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = [
# ]
extensions = [
                # 'recommonmark',
              # 'sphinx_markdown_tables',
              "sphinx.ext.autodoc",
              "sphinx_gallery.load_style",
              "sphinx_autodoc_typehints",
              "sphinx.ext.coverage",
              "sphinx.ext.napoleon",
              "sphinx.ext.todo",
              # "sphinxarg.ext",
              # "sphinxcontrib.autodoc_pydantic",
              "nbsphinx",
              # "enum_tools.autoenum",
              ]

autodoc_member_order = "bysource"
todo_include_todos = False
typehints_defaults = "comma"
autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['**.ipynb_checkpoints']  # 2022/10/18 add


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_logo = "_static/logo.png"
html_theme_options = {"navigation_depth": 4, "logo_only": True}
html_show_sphinx = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']