from utils import WIDTH, get_process_by_name
import tkinter as tk
import subprocess
import os
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
    """the home 'tab' widget of the GUI, where you start the script and where error messages may be shown"""
    def __init__(self, master, *args):
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
                    try:
                        pid = psutil.Process(pid).terminate()
                    except:
                        # it was already terminated, that's fine
                        pass
                    set_pid("")
                else:
                    # create a PyAdScript process, however the process returned is not the one we want
                    # not sure how or why that is, but the returned process is not the correct one
                    try:
                        process = subprocess.Popen(
                            os.path.abspath(r".\PyAdScript.exe"),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            creationflags=subprocess.DETACHED_PROCESS,
                            close_fds=True,
                        )
                    except FileNotFoundError as e:
                        # this means that the script file wasn't found, which is really bad
                        self.handle_error(e)
                        self.running = True  # will be set to False later
                    else:
                        try:
                            out, err = process.communicate(timeout=1)
                            self.handle_error(err)
                            self.running = True  # will be set to False later
                        except subprocess.TimeoutExpired:
                            # this means that the script initialized with no problems
                            process.kill()
                            # re-fetch the script process
                            process = get_process_by_name("PyAdScript.exe")
                            set_pid(process.pid)
                            self.status.set("")
                            # reset cursor and focus
                            root.config(cursor="")
                            btn.config(cursor="hand2")
                            root.focus()

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

    def handle_error(self, err):
        for line in err.split("\n"):
            if ": " in line:
                err_line = line
                break
        else:
            err_line = None

        if err_line is not None:
            err_name = err_line.split(": ")[0]
        else:
            err_name = None

        # spotify path errors
        if err_name == "errors.SpotifyNotFound":
            message = "Spotify executable was unable to be automatically located. Please manually provide the path to Spotify.exe in the settings tab."
        elif err_name == "errors.InvalidPath":
            message = "The path specified for the Spotify executable is invalid. Are you sure the path points to Spotify.exe?"
        elif err_name == "FileNotFoundError":
            message = "The GUI could not find the location of the script (PyAdScript.exe). This means it has been moved, renamed, or deleted. Try re-moving, renaming, or re-installing the script. To reinstall, go to the Guide tab and visit the GitHub for the latest release."
        else:
            message = f"An unknown and unexpected error has occurred during initialization. Make sure all your settings are correct. Go to the script's local directory and open error.txt for more information."
            with open(r".\\error.txt", "w+") as f:
                print(message, file=f)
                print("\nERROR: " + err_name, file=f)
                print(err, file=f)

        self.status.set(message)
