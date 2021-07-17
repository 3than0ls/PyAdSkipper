import tkinter as tk
from utils import Header, Info, Link


class Guide(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
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
        Header(self.frame, text="General Information")._pack()
        general_info = "PyAdSkipper is a tool used to skip Spotify ads. It functions by detecting when your Spotify app is playing an advertisement, automatically closes the Spotify application, relaunches it, and then sends spacebar to the application, which resumes music."
        Info(
            self.frame,
            text=general_info,
        )._pack()
        Link(
            self.frame,
            "Visit this project's GitHub repo",
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
            text="I have just switched Spotify accounts, and the tool is not working.",
        )._pack()
        issues_and_troubleshooting = 'This is because this script caches user information and reuses it rather than asking you or fetching it each time it is started. However, it does mean that if you are switching accounts, the cached information is no longer useful. To fix this, you have to go into the script\'s local directory, and delete all files that start with ".cache".'
        Info(
            self.frame,
            text=issues_and_troubleshooting,
        )._pack()
