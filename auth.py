import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def load_config(filepath="config.json"):

    """Loads the configuration file for the Spotify client.

    It first checks for a 'config_local.json' for local overrides,
    falling back to the provided 'config.json' if it doesn't exist.
    This allows for keeping sensitive credentials out of version control.

    Args:
        filepath (str, optional): The default path to the configuration file.
                                  Defaults to "config.json".

    Returns:
        dict: A dictionary containing the configuration data.
              Returns an empty dictionary if the file cannot be found or
              if there is a JSON decoding error.
    """

    # Use config_local.json for local development overrides if it exists
    file_name = "config_local.json" if os.path.exists("config_local.json") else "config.json"
    with open(file_name, "r") as f:
        return json.load(f)

config = load_config()

def get_spotify_client():

    """Initializes and returns an authenticated Spotify client.

    Uses the credentials and settings from the configuration file loaded
    by load_config(). It sets up the necessary authorization scopes for
    reading private playlists and the user's library.

    Returns:
        spotipy.Spotify or None: An authenticated Spotipy client instance if
                                 configuration is successful, otherwise None.
    """
    
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id= config["client_id"],
                    client_secret= config["client_secret"],
                    redirect_uri= config["redirect_uri"],
                    scope="playlist-read-private playlist-read-collaborative user-library-read"
                    ))