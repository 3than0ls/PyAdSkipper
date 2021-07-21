from utils import (
    locate_spotify_exe,
    get_spotify_pid,
    get_spotify_window_handle,
)
from errors import InvalidPath, SpotifyNotRunning
import json
import time
import win32gui, win32api, win32con
import subprocess
import os
import shutil

VERSION = "1.1"


class Controller:
    # intervals of 0.25 seconds between each loop
    INTERVALS = 0.25

    def __init__(self):
        # set settings variables
        with open(r".\\settings.json", "r") as f:
            self.settings = json.load(f)

        # if no spotify path is provided, try to find it and set. if it is not found in locate_spotify_exe, an error is thrown
        if (
            not self.settings["Spotify Path"]
            or self.settings["Spotify Path"].lower() == "<please specify>"
        ) and (spotify_path := locate_spotify_exe()):
            self.settings["Spotify Path"] = spotify_path
            with open(r".\\settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)

        if not os.path.basename(self.settings["Spotify Path"]) or not shutil.which(
            self.settings["Spotify Path"]
        ):
            raise InvalidPath()

        self.spath = (
            os.path.normpath(self.settings["Spotify Path"])
            .encode("unicode_escape")
            .decode("utf-8")
        )

        # set spotify process ID during initalization
        pid = get_spotify_pid(self.spath)
        if pid is not None:
            self.spotify_pid = pid
        else:
            self.spotify_pid = None

    def is_locked(self):
        # https://stackoverflow.com/a/57258754/9474247
        outputall = str(
            subprocess.check_output(
                "TASKLIST", creationflags=subprocess.CREATE_NO_WINDOW
            )
        )
        return "LogonUI.exe" in outputall

    def restart_spotify(self, spotify_pid=None):
        if spotify_pid is None:
            spotify_pid = get_spotify_pid(self.spath)

        # attempt to close it by clicking out, but if that doesn't work, just terminate the process
        # get the exit handle for spotify, and click it, which exists spotify "gracefully"
        window_handle = get_spotify_window_handle(spotify_pid=spotify_pid)
        win32gui.PostMessage(window_handle, win32con.WM_CLOSE, None, None)

        # used to have a backup to check if it was still open, but now we'll just hope and pray :)

        # wait a little under less than one second after termination to reopen
        time.sleep(0.9)
        # reopen spotify
        spotify_process = subprocess.Popen(self.settings["Spotify Path"])
        self.spotify_pid = spotify_process.pid
        time.sleep(1.9)
        # find window handle and post a space to it to continue playing
        window_handle = get_spotify_window_handle(spotify_pid=self.spotify_pid)
        win32api.PostMessage(window_handle, win32con.WM_KEYDOWN, 0x20, 0)  # post space

        if self.settings["Push To Back"] == "Yes":
            (x, y, w, h) = win32gui.GetWindowRect(window_handle)
            w -= x
            h -= y
            win32gui.SetWindowPos(window_handle, win32con.HWND_BOTTOM, x, y, w, h, 0)

    def currently_playing(self, spotify_pid=None):
        if spotify_pid is None:
            spotify_pid = get_spotify_pid(self.spath)

        if self.spotify_pid is None:
            # Spotify was not running since last iteration, but check again to see if it is
            if spotify_pid is not None:
                self.spotify_pid = spotify_pid
            else:
                # spotify still not open, return None
                return None
        if self.spotify_pid is not None:
            try:
                window_handle = get_spotify_window_handle(spotify_pid=self.spotify_pid)
                window_name = win32gui.GetWindowText(window_handle)
            except SpotifyNotRunning:
                # if it is not running, set spotify_pid to None, and return None
                self.spotify_pid = None
                return None

        # window_name can be a couple of things. it could be "Spotify Free" (when it's paused),
        # "<author> - <song name>" when a song is playing, (so assume it's a song when it's got a dash)
        # and USUALLY "Advertisement" or just "Spotify", or anything else during ads
        if window_name == "Spotify Free" or window_name == "":
            return "<PAUSED>"
        elif " - " in window_name:
            return window_name  # song
        else:
            return "<ADVERTISEMENT>"

    def start(self):
        last_song = ""

        while True:
            if self.settings["Pause When Locked"] == "Yes" and self.is_locked():
                # skip, no need to check
                continue

            spotify_pid = get_spotify_pid(self.spath)
            currently_playing = self.currently_playing(spotify_pid=spotify_pid)
            # print(currently_playing)
            # nothing is being played, so just do nothing
            if currently_playing == "<ADVERTISEMENT>":
                try:
                    self.restart_spotify(spotify_pid=spotify_pid)
                except SpotifyNotRunning:
                    # Spotify was somehow closed by other means before the script could get to it
                    continue
            else:
                if currently_playing != last_song:
                    # print(last_song)
                    last_song = currently_playing

            # do this every interval seconds
            time.sleep(Controller.INTERVALS)


if __name__ == "__main__":
    controller = Controller()
    try:
        controller.start()
    except KeyboardInterrupt as e:
        quit()
