import tkinter as tk
from utils import Header, Info, Link


class Guide(tk.Frame):
    def __init__(self, master, version, *args):
        super().__init__(master)
        self.version = version
        # configure canvas and frame for scroll bar
        self.canvas = tk.Canvas(
            self,
            borderwidth=0,
            highlightthickness=0,
        )
        self.frame = tk.Frame(self.canvas, padx=5, pady=5)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(
            (0, 0), window=self.frame, anchor="nw", tags="self.frame"
        )
        self.frame.bind(
            "<Configure>",
            lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.widget()

    def widget(self):
        Info(
            self.frame,
            text=f"Version {self.version}",
        )._pack()
        Header(self.frame, text="General Information")._pack()
        general_info = f"PyAdSkipper is a tool used to skip Spotify ads. It functions by detecting when an ad is being played, restarting Spotify, and resuming music."
        Info(
            self.frame,
            text=general_info,
        )._pack()
        Link(
            self.frame,
            "Developed by Ethanol",
            "https://github.com/3than0ls",
        )._pack()
        Link(
            self.frame,
            "Visit this project's GitHub repo for more information",
            "https://github.com/3than0ls/PyAdSkipper",
        )._pack()

        Header(self.frame, text="FAQs and Common Issues")._pack()
        Header(
            self.frame,
            text="The tool seems to be having some effect, but doesn't seem to be working correctly.",
        )._pack()
        not_working = "The script has certain intervals in which it executes commands such as restarting Spotify and playing the music. If a computer is under heavy load or is slow, some timed processes and events may be skipped."
        Info(
            self.frame,
            text=not_working,
        )._pack()
