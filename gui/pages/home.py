from utils import WIDTH
import tkinter as tk
import subprocess
import psutil


def set_pid(pid):
    with open("pid.txt", "w+") as f:
        f.write(str(pid))


def get_pid():
    try:
        with open("pid.txt", "r") as f:
            pid = int(f.read())
        if psutil.pid_exists(pid):
            return pid
        else:
            set_pid("")
            raise Exception()
    except:
        set_pid("")
        return None


class Home(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.running = True if get_pid() is not None else False
        self.widget()

    def widget(self):
        self.status = tk.StringVar("")
        label = tk.Label(
            self,
            fg="red",
            pady=10,
            wraplength=WIDTH - 25,
            justify="center",
            textvariable=self.status,
        )
        label.pack(side="top", fill="x")

        # bg_colors, False, True
        status = [
            {"color": "#58e32d", "label": "Start Script", "f": lambda: None},
            {"color": "#e02828", "label": "Stop Script", "f": lambda: None},
        ]

        def on_click(event):
            # change cursor to loading
            btn = event.widget
            root = self.master.master
            root.config(cursor="wait")
            btn.config(cursor="wait")

            # check if the script is actually running, and that they havent task manager closed the script
            pid = get_pid()
            actually_running = True if pid is not None else False
            if self.running == actually_running:
                if actually_running:
                    psutil.Process(pid).terminate()
                    set_pid("")
                else:
                    # subprocess.Popen('script executable path')
                    # might want to put this in a try-except block
                    process = subprocess.Popen(
                        "C:/Users/Ethanol/.virtualenvs/PyAdSkipper-OLyHwyNz/Scripts/python.exe c:/Users/Ethanol/PyAdSkipper/script/index.py",
                        stdin=subprocess.PIPE,
                        # stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                    )
                    # see if any errors were thrown after launch
                    try:
                        _, err = process.communicate(timeout=1)
                        err_line = err.split("\n")[-2]
                        self.running = True  # will be set to False later
                        self.handle_error(err_line, err)
                    except subprocess.TimeoutExpired:
                        # this means that the script is running with no problems (so far)
                        # process.kill()
                        self.status.set("")
                    set_pid(process.pid)
            self.running = not self.running

            btn["activebackground"] = btn["bg"] = status[self.running]["color"]
            btn["text"] = status[self.running]["label"]

            # reset cursor and focus
            root.config(cursor="")
            btn.config(cursor="hand2")
            root.focus()
            # prevent any further tk stuff
            return "break"

        button = tk.Button(
            self,
            text=status[self.running]["label"],  # check if script is running
            command=lambda e: on_click(e),
            padx=50,
            pady=15,
            relief=tk.FLAT,
            foreground="#000",
            activeforeground="#000",
            background=status[self.running]["color"],
            activebackground=status[self.running]["color"],
            cursor="hand2",
        )
        button.pack(side="bottom", fill="x", padx=5, pady=5)
        button.bind("<Button-1>", lambda e: on_click(e))

    def handle_error(self, err_line, err):
        err_name = err_line.split(": ")[0]
        # spotify path errors
        if err_name == "errors.SpotifyNotFound":
            message = "Spotify executable was unable to be automatically located. Please manually provide the path to Spotify.exe in the settings tab."
        elif err_name == "errors.InvalidPath":
            message = "The path specified for the Spotify executable is invalid. Are you sure the path points to Spotify.exe?"
        else:
            message = f"An unknown and unexpected error has occurred during initialization. Make sure all your settings are correct. Go to the script's local directory and open error.txt for more information."
            with open(r".\\errors.txt", "w+") as f:
                print(message, file=f)
                print("\nERROR: " + err_name, file=f)
                print(err, file=f)

        self.status.set(message)