"""
main.py

Application Entry Point

Ramdev Billing Software
"""

import tkinter as tk

from ui.theme import apply_theme
from ui.login_window import LoginWindow


def main():

    root = tk.Tk()

    root.title("Ramdev Billing Software")

    root.geometry("1400x800")

    root.minsize(1200, 700)

    apply_theme(root)

    LoginWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
