# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "MEDIATE"
copyright = "2024, Casper Welzel Andersen, SINTEF"
author = "Casper Welzel Andersen"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_nb",
    # "myst_parser",
    # "nbsphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# master_doc = "contents"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = []
html_theme_options = {
    "navigation_with_keys": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/M-ERA-NET-MEDIATE/DataDocumentation",
            "icon": "fa-brands fa-github",
        },
    ],
    "primary_sidebar_end": ["indices.html"],
    # "switcher": {
    #     "json_url": "_static/versions.json",
    # },
    # "navbar_persistent": ["version-switcher", "search-button"],
}
html_sidebars = {
    "**": ["sidebar-nav-bs"]
}
