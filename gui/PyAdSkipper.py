import sys
from utils import load_settings
import tkinter as tk
from tkinter import ttk
from pages.settings import Settings
from pages.home import Home
from pages.guide import Guide
from utils import WIDTH, HEIGHT
from shortcut import create_desktop_shortcut
from singleton import SingleInstance, SingleInstanceException

VERSION = "1.6"


class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill="x")

        self.menu_widget()

    def menu_widget(self):
        """create the menu widget at the top, allowing multiple 'tabs'"""
        nb = ttk.Notebook(self.master)

        for Page in (Home, Settings, Guide):
            page_name = Page.__name__
            frame = Page(nb, VERSION)
            frame.pack(fill="both", expand=True)
            nb.add(frame, text=page_name)

        nb.pack(fill="both", expand=True)


if __name__ == "__main__":
    # initialize tkinter GUI window
    root = tk.Tk(className=" PyAdSkipper")
    root.resizable(False, False)
    root.geometry(f"{WIDTH}x{HEIGHT}")
    try:
        root.iconbitmap(r".\\icon.ico")
    except:
        pass

    def refocus(event):
        if hasattr(event.widget, "focus"):
            event.widget.focus()

    root.bind_all("<Button-1>", refocus)

    app = Application(root)

    # ensure there is only one instance running
    try:
        me = SingleInstance()
    except SingleInstanceException:
        sys.exit()

    # create a shortcut if setting allows so
    create_shortcut = load_settings()["Create Shortcut"]
    if create_shortcut:
        create_desktop_shortcut()

    # start application
    app.mainloop()
