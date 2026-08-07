"""
base_window.py

Base Window for all modules.

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk

from ui.theme import PRIMARY


class BaseWindow(ttk.Frame):

    def __init__(self, parent, title="", show_header=True):
        super().__init__(parent)

        self.parent = parent
        self.show_header = show_header

        self.pack(fill="both", expand=True)

        if self.show_header:
            self.create_header(title)
        self.create_toolbar()
        self.create_content()
        self.create_statusbar()

    # -------------------------------------------------
    # Header
    # -------------------------------------------------

    def create_header(self, title):

        header = ttk.Frame(
            self,
            style="Card.TFrame",
            padding=(18, 16)
        )

        header.pack(fill="x", padx=16, pady=(16, 10))

        accent = tk.Frame(
            header,
            width=5,
            bg=PRIMARY,
            bd=0,
            highlightthickness=0
        )

        accent.pack(side="left", fill="y", padx=(0, 16))

        text_block = ttk.Frame(
            header,
            style="Card.TFrame"
        )

        text_block.pack(side="left", fill="x", expand=True)

        lbl = ttk.Label(
            text_block,
            text=title,
            style="Header.TLabel"
        )

        lbl.pack(anchor="w")

        subtitle = ttk.Label(
            text_block,
            text="A cleaner workspace for faster billing and management.",
            style="Subtitle.TLabel"
        )

        subtitle.pack(anchor="w", pady=(4, 0))

    # -------------------------------------------------
    # Toolbar
    # -------------------------------------------------

    def create_toolbar(self):

        self.toolbar = ttk.Frame(
            self,
            style="Toolbar.TFrame",
            padding=(16, 0, 16, 10)
        )

        self.toolbar.pack(
            fill="x",
            padx=0,
            pady=(0, 0)
        )

    # -------------------------------------------------
    # Content
    # -------------------------------------------------

    def create_content(self):

        self.content = ttk.Frame(
            self,
            style="Card.TFrame",
            padding=16
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(0, 12)
        )

    # -------------------------------------------------
    # Status Bar
    # -------------------------------------------------

    def create_statusbar(self):

        self.status = tk.StringVar()

        self.status.set("Ready")

        bar = ttk.Label(
            self,
            textvariable=self.status,
            style="Status.TLabel",
            anchor="w"
        )

        bar.pack(fill="x", side="bottom", padx=16, pady=(0, 14))

    # -------------------------------------------------

    def set_status(self, text):

        self.status.set(text)
