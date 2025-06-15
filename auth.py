import json
import os
import spotipy
import logging
import sys
from spotipy.oauth2 import SpotifyOAuth

def load_config():

    """Loads the configuration from a file.

    This function first checks for a 'config_local.json' file for local
    overrides. If not found, it falls back to 'config.json'. This allows for
    keeping sensitive credentials in a local file that is not checked into
    version control.

    The program will exit if the configuration file is not found or if
    it contains invalid JSON.

    Returns:
        dict: A dictionary containing the configuration data.

    Raises:
        SystemExit: If the configuration file cannot be found or decoded.
    """

    # Use config_local.json for local development overrides if it exists
    file_name = "config_local.json" if os.path.exists("config_local.json") else "config.json"
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Config File '{file_name}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error(f"Could not decode '{file_name}'")
        sys.exit(1)


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