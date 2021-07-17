import getpass
from pathlib import Path
import psutil
import win32gui
import win32process
import pywintypes
import os
import subprocess
from errors import SpotifyNotFound, SpotifyNotRunning


def locate_spotify_exe():
    user = getpass.getuser()
    dirs = [
        rf"C:\\Users\\{user}\\AppData\\Roaming\\Spotify",
        r"C:\\Program Files\\Spotify",
    ]
    spotify_path = None

    def search(path):
        if path.exists() and path.is_dir():
            for root, _, files in os.walk(dir):
                lowered = [file.lower() for file in files]
                try:
                    i = lowered.index("spotify.exe")
                    return os.path.join(root, files[i])
                except ValueError:
                    pass
        return None

    for dir in dirs:
        path = Path(dir)
        spotify_path = search(path)
        # return first find
        if spotify_path is not None:
            return spotify_path
    else:
        raise SpotifyNotFound()


def _psutil_get_spotify_pid():
    # WMIC is not found, try psutil method instead
    name = "Spotify.exe"
    process = None
    for p in psutil.process_iter():
        name_, exe, cmdline = "", "", []
        try:
            name_ = p.name()
            cmdline = p.cmdline()
            exe = p.exe()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except psutil.NoSuchProcess:
            continue
        if name == name_ or os.path.basename(exe) == name:
            if len(cmdline) == 1:
                process = p
    if process is None:
        # raise SpotifyNotRunning()
        return None
    else:
        return process.id


def get_spotify_pid(spotify_path):
    # spotify path should be similar to: 'C:\\Users\\<user>\\AppData\\Roaming\\Spotify\\Spotify.exe' or other
    if spotify_path is None:
        return _psutil_get_spotify_pid()

    try:
        outputs = subprocess.check_output(
            [
                r"C:\\Windows\\System32\\wbem\\WMIC.exe",
                "process",
                "where",
                "ExecutablePath='" + spotify_path + "'",
                "get",
                "ProcessId",
            ],
            encoding="utf-8",
        )
        outputs = outputs.strip().split("ProcessId")[1].split()
        if outputs:
            return int(outputs[0])
        else:
            return None
    except IndexError:
        return None
    # WMIC is not on this system, use the alt method
    except FileNotFoundError:
        return _psutil_get_spotify_pid()


_handle = None


def _callback(hwnd, spotify_pid):
    global _handle
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == spotify_pid:
        rect = win32gui.GetWindowRect(hwnd)
        if rect != (0, 0, 0, 0) and rect != (0, 0, 1, 1):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text != "":
                _handle = hwnd
                return False


_keywords = ["Spotify Free", "Spotify.exe", "Advertisement"]


def get_spotify_window_handle(spotify_pid):
    global _handle
    _handle = None

    # attempt to search for it by it's paused (or newly reopened) state where the window name is Spotify Free, or other keywords
    for keyword in _keywords:
        _handle = win32gui.FindWindow(None, keyword)
        if _handle != 0:
            return _handle

    try:
        win32gui.EnumWindows(_callback, spotify_pid)
    except pywintypes.error:
        pass

    if _handle is not None:
        return _handle
    else:
        raise SpotifyNotRunning()
