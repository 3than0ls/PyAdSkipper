class SpotifyNotFound(Exception):
    """When Spotify path is not specified and Spotify cannot be found"""

    def __init__(self):
        super().__init__(
            "Spotify executable was unable to be automatically located. Please manually provide the path to Spotify.exe in the settings tab."
        )


class SpotifyNotRunning(Exception):
    """When Spotify is not running when it needs to be, throw this error"""

    def __init__(self):
        super().__init__("Spotify is not running.")


class InvalidPath(Exception):
    """When Spotify path points to an invalid file that isn't an executable or isn't named Spotify"""

    def __init__(self):
        super().__init__(
            "The path specified for the Spotify executable is invalid. Are you sure the path points to Spotify.exe?"
        )
