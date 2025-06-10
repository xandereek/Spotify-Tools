import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def load_config(filepath="config.json"):
    file_name = "config_local.json" if os.path.exists("config_local.json") else "config.json"
    with open(file_name, "r") as f:
        return json.load(f)

config = load_config()

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id= config["client_id"],
                    client_secret= config["client_secret"],
                    redirect_uri= config["redirect_uri"],
                    scope="playlist-read-private playlist-read-collaborative user-library-read"
                    ))