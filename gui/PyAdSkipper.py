from gui.utils import load_settings
import tkinter as tk
from tkinter import ttk
from pages.settings import Settings
from pages.home import Home
from pages.guide import Guide
from utils import WIDTH, HEIGHT
from shortcut import create_desktop_shortcut
import os

VERSION = "1.3"


class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill="x")

        self.menu_widget()

    def menu_widget(self):
        nb = ttk.Notebook(self.master)

        for Page in (Home, Settings, Guide):
            page_name = Page.__name__
            frame = Page(nb, VERSION)
            frame.pack(fill="both", expand=True)
            nb.add(frame, text=page_name)

        nb.pack(fill="both", expand=True)


if __name__ == "__main__":
    create_shortcut = load_settings()["Create Shortcut"]
    if create_shortcut:
        create_desktop_shortcut()
    else:
        shortcut_path = os.path.join(os.path.expanduser("~/Desktop"), "PyAdSkipper.lnk")
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)

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
    app.mainloop()
