import tkinter as tk
from utils import Header, Info, Link


class Guide(tk.Frame):
    def __init__(self, master, version, *args):
        """the guide 'tab' widget of the GUI"""
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
        general_info = f"PyAdSkipper is a tool used to skip Spotify ads. It functions by detecting when an ad is being played, restarting Spotify, and resuming music. View the README included in the local directory for the most information."
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
            "Visit this project's GitHub repo for more information.",
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

        Header(
            self.frame,
            text="The script does not seem to be skipping some ads.",
        )._pack()
        not_skipping = 'The script relies on the Spotify window name to recognize if an ad is playing, meaning there is no need to use the Spotify API (which woud require additional bothersome credentials.) The downside, however, is that while for most ads, the window name is "Advertisement," some ads (usually those from Spotify artist/songs) are not named this, and so the script does not detect that they are ads. Unfortunately, there is no current way to solve this.'
        Info(
            self.frame,
            text=not_skipping,
        )._pack()

        Header(
            self.frame,
            text="The script is skipping my local file songs.",
        )._pack()
        skipping_local = 'Again, the script relies on the Spotify window name to recognize if an ad is playing. The window name of Spotify when playing a local file is the name of that local file. If you name your local file "Advertisement", it will automatically be considered an advertisement.'
        Info(
            self.frame,
            text=skipping_local,
        )._pack()
