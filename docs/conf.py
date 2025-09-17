# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
project = "greencell-client"
author = "Jakub Brzezowski"
copyright = ""
root_doc = "index"
try:
    from greencell_client import __version__ as release
except Exception:
    release = ""

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_autodoc_typehints",
]

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "member-order": "bysource"
}
napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_theme_options = {
    "light_logo": "icon.png",
    "dark_logo": "dark_icon.png",
    "light_css_variables": {
        # branding
        "color-brand-primary": "#149653",
        "color-brand-content": "#149653",

        # tła
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8fafc",
        "color-background-hover": "#f1f5f9",
        "color-background-border": "#e5e7eb",

        # teksty
        "color-foreground-primary": "#052614",
        "color-foreground-secondary": "#313238",
        "color-foreground-muted": "#5c5f6d",

        # linki
        "color-link": "#0ea5e9",
        "color-link--hover": "#0284c7",

        # kod inline
        "color-inline-code-background": "#f3f4f6",
        "color-inline-code-foreground": "#111827",

        # nawigacja / panele
        "color-sidebar-background": "#fafafa",
        "color-sidebar-border": "#fafafa",
        "color-toc-background": "#fafafa",
    },
    "dark_css_variables": {
        "color-brand-primary": "#38bdf8",
        "color-brand-content": "#38bdf8",

        "color-background-primary": "#171717",
        "color-background-secondary": "#222222",
        "color-background-hover": "#313238",
        "color-background-border": "#313238",

        "color-foreground-primary": "#e5e7eb",
        "color-foreground-secondary": "#cbd5e1",
        "color-foreground-muted": "#94a3b8",

        "color-link": "#0A739A",
        "color-link--hover": "#18B2DF",

        "color-inline-code-background": "#1f2937",
        "color-inline-code-foreground": "#e5e7eb",

        "color-sidebar-background": "#00392C",
        "color-sidebar-secondary": "#313238",
        "color-sidebar-border": "#313238",
        "color-toc-background": "#222222",

    },
}
html_static_path = ["_static"]
