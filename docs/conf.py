# Copyright (c) 2025 csg-sa

# -- Path setup --------------------------------------------------------------
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
project = "greencell-client"
author = "CSG SA"
copyright = f"{date.today().year} CSG SA — MIT License"
root_doc = "index"
try:
    from greencell_client import __version__ as release
except ImportError:
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
autodoc_default_options = {"members": True, "undoc-members": True, "member-order": "bysource"}
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
        "color-brand-primary": "#149653",
        "color-brand-content": "#149653",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8fafc",
        "color-background-hover": "#f1f5f9",
        "color-background-border": "#e5e7eb",
        "color-foreground-primary": "#052614",
        "color-foreground-secondary": "#313238",
        "color-foreground-muted": "#5c5f6d",
        "color-link": "#0ea5e9",
        "color-link--hover": "#0284c7",
        "color-inline-code-background": "#f3f4f6",
        "color-inline-code-foreground": "#111827",
        "color-sidebar-background": "#fafafa",
        "color-sidebar-border": "#fafafa",
        "color-toc-background": "#fafafa",
    },
    "dark_css_variables": {
        "color-brand-primary": "#149653",
        "color-brand-content": "#1ABD69",
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
    "footer_icons": [
        {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
            "html": '<span style="font-weight:600;">License</span>',
            "class": "",
        },
    ],
}
html_static_path = ["_static"]
