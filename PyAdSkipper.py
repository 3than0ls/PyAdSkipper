import spotipy
import json
import time
from spotipy.oauth2 import SpotifyOAuth
import win32gui
import win32api
import win32con
import requests
import subprocess
import os
import re
import getpass


last_input = win32api.GetLastInputInfo()
last_active = time.time()



CLIENT_ID = "6048c9d95dc74ed7bae279a4e1f1aaca"
CLIENT_SECRET = "e22ce642867b4259af1e853584588dc8"
REDIRECT_URI = "http://127.0.0.1:8000"
SCOPE = "user-read-playback-state user-library-read user-top-read"
USERNAME = "Ethanol"

    
class Controller:
    def __init__(self, id, secret, uri, scope, username):
        self.current_playing_name = None
        
        self.handle = None

        self.id = id
        self.secret = secret
        self.uri = uri
        self.scope = scope
        self.username = username

        self.oauth = self.create_OAuth(id, secret, uri, scope, username)
        self.token_data = None
        self.spotify = spotipy.Spotify(auth_manager=self.oauth)

        self.running = True

    @staticmethod
    def log_response(data):
        with open("data.json", "w+") as f:
            json.dump(data, f, indent=4)

    def create_OAuth(self, id, secret, uri, scope, username):
        return SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri=uri, scope=scope, username=username)

    
    def find_spotify_window(self):
        handles = []
        def callback(hwnd, a):
            if re.match(a, str(win32gui.GetWindowText(hwnd))) is not None:
                handles.append(hwnd)
        win32gui.EnumWindows(callback, ".*Spotify Free*")
        if handles:
            self.handle = handles[0]

    def restart_connection(self):
        print("restarting connection")
        self.spotify = spotipy.Spotify(auth_manager=self.create_OAuth(self.id, self.secret, self.uri, self.scope, self.username))

    def close(self):
        """closes all spotify tasks"""
        os.system(f'taskkill /f /im spotify.exe')

    def open(self):
        """opens a spotify task"""
        return subprocess.Popen("spotify")

    def reopen_and_replay(self):
        time.sleep(2.5)
        self.close()
        self.open()
        time.sleep(2.5)
        self.find_spotify_window()
        time.sleep(2.5)
        win32api.PostMessage(self.handle, win32con.WM_KEYDOWN, 0x20, 0) # post space

        # perhpaps a while loop testing if song is playing, and if not, every x interval post message

    def run(self):
        while self.running:
            if win32api.GetLastInputInfo() != last_input: # if active
                try:
                    currently_playing = self.spotify.currently_playing()
                    
                    if currently_playing is not None:
                        if currently_playing['currently_playing_type'] == 'track':
                            if self.current_playing_name != currently_playing['item']['name']:
                                print(f"Now playing {currently_playing['item']['name']}")
                                self.current_playing_name = currently_playing['item']['name']

                        elif currently_playing['currently_playing_type'] == 'ad':
                            print('playing an ad')
                            if next((device for device in self.spotify.devices()["devices"] if device["name"] == os.environ['COMPUTERNAME'] and device["type"] == "Computer"), None):
                                self.reopen_and_replay()
                except Exception as e:
                    print("error", e)
                    self.restart_connection()

                time.sleep(0.2)
    



controller = Controller(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE, USERNAME)
try:
    controller.run()
except KeyboardInterrupt as e:
    quit()