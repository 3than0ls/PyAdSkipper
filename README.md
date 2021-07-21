# PyAdSkipper
A python script that skips Spotify ads, and can be launched through a GUI. Uses pywin32, and only works for Windows.

# How does it work?
This script skips Spotify ads by detecting when the Spotify application is playing an ad, gracefully closing Spotify, re-opening it, and sending a spacebar message to it, which resumes playing.
Note that due to complications unfortunately out of this script's control, some Spotify ads are not detected as ads and aren't skipped.


# PyAdSkipper settings
Application settings can be changed using the GUI. Manually changing the values may result in some things not working. If this is the case, just delete `settings.json` and a new one with default settinsg will be automatically generated.

`Spotify Path` - `Windows path to Spotify.exe` - This is the path to Spotify.exe on your computer. If not specified, the script will attempt to locate Spotify.exe at the paths `"C:\\Users\\<user>\\AppData\\Roaming\\Spotify"` and `"C:\\Program Files\\Spotify"`. If it still can't find it, the script will throw an error that will be shown on the GUI home screen.

`Speed` - `Fast`, `Medium`, or `Slow` - Some computers may be faster or slower than others. This settings affects the time between when an attempt to launch a Spotify process/window/application occurs and when to post the spacebar message. Slower computers may take a while to start Spotify (and in the worst case scenario, start Spotify in a non-functional state or not at all). However, this doesn't guarantee everything will work. On slower computers or computers under heavy load, certain events may be skipped or delayed, causing the script to not skip ads properly.

`Pause When Locked` - `Yes` or `No` - This setting changes whether or not the script will check if an ad is playing when the Windows account is locked. This was created because it would cause certain complicated and niche issue when using Spotify desktop and Spotify mobile concurrently. It's reccomended to set this to `Yes` if you do use Spotify mobile while the Spotify desktop application is running, otherwise, it's up to you.

`Pause When Locked` - `Yes` or `No` - If set to `Yes`, Spotify will be pushed below the active window and not cover it after restarting.

`Create Shortcut` - `Yes` or `No` - If set to `Yes`, a new desktop shortcut will be created (and possibly override the previous one) in the desktop folder. If set to no, shortcut deletion be stopped, but the current desktop shortcut will not be deleted.

# Packages and Python version
PyAdSkipper runs on Python 3.8
PyAdSkipper relies on `pywin32` for interaction with handles to the Spotify window, and `psutil` to get information about running processes.
PyAdSkipper also uses `pyinstaller` to compile the script into an executable, and `black` to format code, but these are developer dependencies

# Compiling the script and GUI to 2 seperate executables
Install all dependencies and dev dependencies specified by the Pipfile, and then run these two commands.
1) `pyinstaller -F -i .\icon.ico -w .\gui\PyAdSkipper.py`
2) `pyinstaller -F -i .\icon.ico -w .\script\PyAdScript.py`
Then, move `icon.ico` to the created `dist` folder. After running it the first time, a `settings.json` file and `pid.txt` file will be generated.