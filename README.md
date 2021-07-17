# PyAdSkipper
A python script that skips Spotify ads, and can be launched through a GUI. Uses pywin32, and only works for Windows.

# How does it work?
This script skips Spotify ads by detecting when the Spotify application is playing an ad, gracefully closing Spotify, re-opening it, and sending a spacebar message to it, which resumes playing.

# PyAdSkipper Settings
Application settings can be changed using the GUI. Manually changing the values may result in some things not working. If this is the case, just delete `settings.json` and a new one with default settinsg will be automatically generated.

**`Spotify Path`** - `Windows path to Spotify.exe` - This is the path to Spotify.exe on your computer. If not specified, the script will attempt to locate Spotify.exe at the paths `"C:\\Users\\<user>\\AppData\\Roaming\\Spotify"` and `"C:\\Program Files\\Spotify"`. If it still can't find it, the script will throw an error that will be shown on the GUI home screen.

**`Speed`** - `Fast`, `Medium`, or `Slow` - Some computers may be faster or slower than others. This settings affects the time between when an attempt to launch a Spotify process/window/application occurs and when to post the spacebar message. Slower computers may take a while to start Spotify (and in the worst case scenario, start Spotify in a non-functional state or not at all). However, this doesn't guarantee everything will work. On slower computers or computers under heavy load, certain events may be skipped or delayed, causing the script to not skip ads properly.

**`Pause When Locked`** - `Yes` or `No` - This setting changes whether or not the script will check if an ad is playing when the Windows account is locked. This was created because it would cause certain complicated and niche issue when using Spotify desktop and Spotify mobile concurrently. It's reccomended to set this to `Yes` if you do use Spotify mobile while the Spotify desktop application is running, otherwise, it's up to you.

**`Pause When Locked`** - `Yes` or `No` - If set to `Yes`, Spotify will be pushed below the active window and not cover it after restarting.

# Packages
PyAdSkipper relies on `pywin32` for interaction with handles to the Spotify window, and `psutil` to get information about running processes.