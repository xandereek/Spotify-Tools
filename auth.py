import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets_1 import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id= CLIENT_ID,
                    client_secret= CLIENT_SECRET,
                    redirect_uri= REDIRECT_URI,
                    scope="playlist-read-private playlist-read-collaborative user-library-read"
                    ))