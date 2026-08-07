"""
theme.py

Global UI Theme

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk


# ==========================================================
# Colors
# ==========================================================

PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"

SUCCESS = "#2E7D32"
WARNING = "#ED6C02"
DANGER = "#D32F2F"

BACKGROUND = "#EEF3F9"
SURFACE = "#FFFFFF"
SURFACE_ALT = "#F5F7FB"

TEXT = "#111827"
TEXT_LIGHT = "#6B7280"

BORDER = "#D7E0EA"

SIDEBAR = "#0F172A"
SIDEBAR_TEXT = "#FFFFFF"


# ==========================================================
# Fonts
# ==========================================================

FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
TITLE_FONT = ("Segoe UI", 18, "bold")
HEADER_FONT = ("Segoe UI", 11, "bold")
SUBTITLE_FONT = ("Segoe UI", 10)


# ==========================================================
# Theme
# ==========================================================

def apply_theme(root):

    style = ttk.Style(root)

    style.theme_use("clam")

    root.configure(bg=BACKGROUND)

    # ------------------------------------------------------
    # Frame
    # ------------------------------------------------------

    style.configure(
        "TFrame",
        background=BACKGROUND
    )

    style.configure(
        "Card.TFrame",
        background=SURFACE,
        borderwidth=1,
        relief="flat"
    )

    style.configure(
        "Content.TFrame",
        background=BACKGROUND
    )

    style.configure(
        "Toolbar.TFrame",
        background=BACKGROUND
    )

    style.configure(
        "Sidebar.TFrame",
        background=SIDEBAR
    )

    style.configure(
        "Hero.TFrame",
        background=SIDEBAR
    )

    style.configure(
        "Card.TLabelframe",
        background=SURFACE,
        borderwidth=1,
        relief="flat"
    )

    style.configure(
        "Card.TLabelframe.Label",
        background=SURFACE,
        foreground=PRIMARY,
        font=HEADER_FONT
    )

    # ------------------------------------------------------
    # Label
    # ------------------------------------------------------

    style.configure(
        "TLabel",
        background=BACKGROUND,
        foreground=TEXT,
        font=FONT
    )

    style.configure(
        "Header.TLabel",
        background=BACKGROUND,
        foreground=TEXT,
        font=TITLE_FONT
    )

    style.configure(
        "Subtitle.TLabel",
        background=BACKGROUND,
        foreground=TEXT_LIGHT,
        font=SUBTITLE_FONT
    )

    style.configure(
        "Muted.TLabel",
        background=BACKGROUND,
        foreground=TEXT_LIGHT,
        font=FONT
    )

    style.configure(
        "Card.TLabel",
        background=SURFACE,
        foreground=TEXT,
        font=FONT_BOLD
    )

    style.configure(
        "CardHeader.TLabel",
        background=SURFACE,
        foreground=TEXT,
        font=TITLE_FONT
    )

    style.configure(
        "CardSubtitle.TLabel",
        background=SURFACE,
        foreground=TEXT_LIGHT,
        font=SUBTITLE_FONT
    )

    style.configure(
        "CardSection.TLabel",
        background=SURFACE,
        foreground=PRIMARY,
        font=HEADER_FONT
    )

    style.configure(
        "CardMuted.TLabel",
        background=SURFACE,
        foreground=TEXT_LIGHT,
        font=FONT
    )

    style.configure(
        "Sidebar.TLabel",
        background=SIDEBAR,
        foreground=SIDEBAR_TEXT,
        font=FONT
    )

    style.configure(
        "SidebarMuted.TLabel",
        background=SIDEBAR,
        foreground="#94A3B8",
        font=FONT
    )

    style.configure(
        "SidebarNav.TLabel",
        background=SIDEBAR,
        foreground=SIDEBAR_TEXT,
        font=FONT_BOLD,
        padding=(14, 10)
    )

    style.configure(
        "SidebarNavActive.TLabel",
        background="#111C34",
        foreground=SIDEBAR_TEXT,
        font=FONT_BOLD,
        padding=(14, 10)
    )

    style.configure(
        "Section.TLabel",
        background=BACKGROUND,
        foreground=PRIMARY,
        font=HEADER_FONT
    )

    style.configure(
        "Status.TLabel",
        background=BACKGROUND,
        foreground=TEXT_LIGHT,
        font=FONT,
        padding=(12, 8)
    )

    # ------------------------------------------------------
    # LabelFrame
    # ------------------------------------------------------

    style.configure(
        "TLabelframe",
        background=BACKGROUND,
        borderwidth=1,
        relief="flat"
    )

    style.configure(
        "TLabelframe.Label",
        background=BACKGROUND,
        foreground=PRIMARY,
        font=HEADER_FONT
    )

    # ------------------------------------------------------
    # Entry
    # ------------------------------------------------------

    style.configure(
        "TEntry",
        padding=10,
        font=FONT,
        fieldbackground=SURFACE,
        background=SURFACE,
        foreground=TEXT,
        bordercolor=BORDER
    )

    # ------------------------------------------------------
    # Combobox
    # ------------------------------------------------------

    style.configure(
        "TCombobox",
        padding=10,
        font=FONT,
        fieldbackground=SURFACE,
        background=SURFACE,
        foreground=TEXT,
        bordercolor=BORDER
    )

    style.configure(
        "TCheckbutton",
        background=BACKGROUND,
        foreground=TEXT,
        font=FONT
    )

    style.configure(
        "Card.TCheckbutton",
        background=SURFACE,
        foreground=TEXT_LIGHT,
        font=FONT,
        padding=0
    )

    # ------------------------------------------------------
    # Buttons
    # ------------------------------------------------------

    style.configure(
        "TButton",
        font=FONT_BOLD,
        padding=(14, 10),
        background=PRIMARY,
        foreground="white",
        borderwidth=0
    )

    style.configure(
        "Accent.TButton",
        font=FONT_BOLD,
        padding=(14, 10),
        background=PRIMARY,
        foreground="white",
        borderwidth=0
    )

    style.configure(
        "Outline.TButton",
        font=FONT_BOLD,
        padding=(14, 10),
        background=SURFACE,
        foreground=PRIMARY,
        bordercolor=PRIMARY,
        relief="flat"
    )

    style.configure(
        "Ghost.TButton",
        font=FONT_BOLD,
        padding=(14, 10),
        background=BACKGROUND,
        foreground=TEXT,
        borderwidth=0
    )

    style.configure(
        "Sidebar.TButton",
        font=FONT_BOLD,
        padding=(16, 12),
        anchor="w",
        foreground=SIDEBAR_TEXT,
        background=SIDEBAR,
        borderwidth=0
    )

    style.map(
        "TButton",
        background=[
            ("active", PRIMARY_DARK),
            ("!disabled", PRIMARY)
        ],
        foreground=[
            ("!disabled", "white")
        ]
    )

    style.map(
        "Accent.TButton",
        background=[
            ("active", PRIMARY_DARK),
            ("!disabled", PRIMARY)
        ],
        foreground=[
            ("!disabled", "white")
        ]
    )

    style.map(
        "Outline.TButton",
        background=[
            ("active", SURFACE_ALT),
            ("!disabled", SURFACE)
        ],
        foreground=[
            ("!disabled", PRIMARY)
        ]
    )

    style.map(
        "Ghost.TButton",
        background=[
            ("active", SURFACE_ALT),
            ("!disabled", BACKGROUND)
        ],
        foreground=[
            ("!disabled", TEXT)
        ]
    )

    style.map(
        "Sidebar.TButton",
        background=[
            ("active", PRIMARY),
            ("!disabled", SIDEBAR)
        ],
        foreground=[
            ("!disabled", SIDEBAR_TEXT)
        ]
    )

    # ------------------------------------------------------
    # Treeview
    # ------------------------------------------------------

    style.configure(
        "Treeview",
        rowheight=30,
        font=FONT,
        background=SURFACE,
        fieldbackground=SURFACE,
        bordercolor=BORDER,
        relief="flat"
    )

    style.configure(
        "Treeview.Heading",
        font=FONT_BOLD,
        background=PRIMARY,
        foreground="white",
        relief="flat"
    )

    style.map(
        "Treeview.Heading",
        background=[
            ("active", PRIMARY_DARK)
        ]
    )

    style.map(
        "Treeview",
        background=[
            ("selected", PRIMARY)
        ],
        foreground=[
            ("selected", "white")
        ]
    )

    # ------------------------------------------------------
    # Notebook
    # ------------------------------------------------------

    style.configure(
        "TNotebook",
        background=BACKGROUND
    )

    style.configure(
        "TNotebook.Tab",
        padding=(15, 8),
        font=FONT_BOLD
    )

    # ------------------------------------------------------
    # Scrollbar
    # ------------------------------------------------------

    style.configure(
        "Vertical.TScrollbar",
        gripcount=0,
        background=BORDER,
        troughcolor=BACKGROUND,
        bordercolor=BACKGROUND,
        arrowcolor=TEXT_LIGHT
    )


# ==========================================================
# Sidebar Button
# ==========================================================

def sidebar_button(parent, text, command):

    return ttk.Button(

        parent,

        text=text,

        command=command,

        style="Sidebar.TButton"
    )
