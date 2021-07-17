import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import webbrowser
import json


### WIDTH and HEIGHT of the GUI window
WIDTH = 420
HEIGHT = 170


### utility functions to save and load settings
def save_settings(settings):
    with open("settings.json", "w+") as f:
        json.dump(settings, f, indent=4)


def load_settings(path="settings.json"):
    try:
        with open(path, "r") as f:
            return json.loads(f.read())
    except:
        default_settings = {
            "Spotify Path": "<Please specify>",
            "Speed": "Medium",
            "Pause When Locked": "Yes",
            "Push To Back": "Yes",
        }
        save_settings(default_settings)
        return default_settings


#### A bunch of components used in the GUI


class Input(tk.Entry):
    """me tryna wrestle in components as if tkinter was react"""

    def __init__(self, master, name, value="", on_change=lambda new_value: None):
        sv = tk.StringVar(value=value)
        sv.trace("w", lambda *_, sv=sv: self._on_change())
        self.sv = sv
        self.on_change = on_change
        self.name = name

        super().__init__(master, textvariable=self.sv)

    def _on_change(self):
        # may want to apply extra code here
        # if self.get() != self._cache:
        self.on_change(self.get())


class Dropdown(ttk.Combobox):
    def __init__(
        self, master, name, options, default_index=0, on_change=lambda new_value: None
    ):
        sv = tk.StringVar(value=options[default_index])
        sv.trace("w", lambda *_, sv=sv: self._on_change())
        self.sv = sv
        self.on_change = on_change
        self.name = name
        super().__init__(master, state="readonly", textvariable=self.sv, values=options)

    def _on_change(self):
        # may want to apply extra code here
        # if self.get() != self._cache:
        self.on_change(self.sv.get())
        self.master.master.focus()


class FileSelector(tk.Button):
    def __init__(self, master, name, value="", on_change=lambda: None):
        # sv is the file
        sv = tk.StringVar(value=value)
        self.sv = sv
        self.on_change = on_change
        self.name = name

        def callback():
            filename = askopenfilename()
            self.master.focus()
            if filename:
                self.sv.set(filename)
            self.on_change(None)

        pixel = tk.PhotoImage(width=100, height=15)

        super().__init__(
            master,
            anchor="w",
            textvariable=self.sv,
            text=sv,
            command=lambda *_: callback(),
            relief=tk.SOLID,
            border=1,
            image=pixel,
            width=100,
            height=15,
            compound="c",
            bg="#fff",
        )
        self.bind("<Button-1>", lambda *_: callback())

    def _pack(self):
        self.pack(
            anchor=tk.NW,
        )
        return self


class CreateToolTip(object):
    # Copied from https://stackoverflow.com/a/36221216/9474247
    def __init__(self, widget, text=""):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            self.tw,
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            wraplength=self.wraplength,
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class Header(tk.Label):
    def __init__(self, master, text):
        super().__init__(
            master,
            text=text,
            font=("helvetica", "10", "bold"),
            wraplength=WIDTH - 40,
        )

    def _pack(self):
        self.pack(anchor=tk.NW)
        return self


class Info(tk.Label):
    def __init__(self, master, text):
        super().__init__(master, text=text, wraplength=WIDTH - 40, justify="left")

    def _pack(self):
        self.pack(
            anchor=tk.NW,
        )
        return self


class Link(tk.Label):
    def __init__(self, master, text, hyperlink):
        super().__init__(
            master,
            text=text,
            wraplength=WIDTH - 40,
            fg="blue",
            cursor="hand2",
        )

        def callback(link):
            webbrowser.open_new(link)

        self.bind("<Button-1>", lambda _: callback(hyperlink))

    def _pack(self):
        self.pack(anchor=tk.NW)
        return self
