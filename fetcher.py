import logging
import requests
import time
from tqdm import tqdm
from spotipy import SpotifyException

def playlist_fetcher(sp, playlist_id):

    """Fetches all tracks from a Spotify playlist and yields them one by one.

    This function iterates through a Spotify playlist, handling pagination automatically.
    It shows a progress bar using tqdm.

    Args:
        sp (spotipy.Spotify): An authenticated Spotipy client instance.
        playlist_id (str): The ID of the Spotify playlist to fetch tracks from.

    Yields:
        tuple[str, str]: A tuple containing the track name and the primary artist's name.
    """

    logging.info("Fetching playlist data..")

    try:
        response = sp.playlist_tracks(playlist_id, limit=1)
        total = response.get('total', 0)
    except (SpotifyException, requests.exceptions.RequestException) as e:
        logging.error(f"Error fetching playlist data: {e}")
        return
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return



    limit = 100
    offset = 0

    with tqdm(total=total, desc="Fetching Playlist", unit="track") as pbar:
        while True:
            max_retries = 3
            attempt = 0
            items = None
            while attempt < max_retries:
                try:
                    response = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
                    items = response['items']
                    break
                except (SpotifyException, requests.exceptions.RequestException) as e:
                    attempt += 1
                    logging.warning(f"Error getting tracks Attempt{attempt}: {e}")
                    if attempt == max_retries:
                        logging.error("Failed getting tracks")
                        break
                    time.sleep(1)

            if not items:
                break

            for i in items:
                track = i.get('track')
                if track:
                    track_name = track.get('name', 'Unknown Track')
                    artists = track.get('artists')
                    if artists:
                        artist_name = artists[0].get('name', 'Unknown Artist')
                    else:
                        artist_name = 'Unknown Artist'

                    yield (track_name, artist_name)
                
            offset += limit
            pbar.update(len(items))

def fetch_liked_songs(sp):

    """Fetches all of the current user's liked songs from Spotify and yields them.

    This generator function paginates through the user's saved tracks,
    displaying a progress bar during the process.

    Args:
        sp (spotipy.Spotify): An authenticated Spotipy client instance.

    Yields:
        tuple[str, str]: A tuple containing the track name and the primary artist's name.
    """
    
    logging.info("Fetching liked songs..")
    response = sp.current_user_saved_tracks(limit=1)
    total = response.get('total', 0)

    limit = 50
    offset = 0
    with tqdm(total=total, desc="Fetching liked songs", unit="track") as pbar:
        while True:
            max_retries = 3
            attempt = 0
            items = None
            while attempt < max_retries:
                try:
                    response = sp.current_user_saved_tracks(limit=limit, offset=offset)
                    items = response['items']
                    break
                except (SpotifyException, requests.exceptions.RequestException) as e:
                    attempt += 1
                    logging.warning(f"Error getting tracks Attempt{attempt}: {e}")
                    if attempt == max_retries:
                        break
                    time.sleep(1)

            if not items:
                break

            for i in items:
                track = i.get('track')
                if track:
                    track_name = track.get('name', 'Unknown Track')
                    artists = track.get('artists')
                    if artists:
                        artist_name = artists[0].get('name', 'Unknown Artist')
                    else:
                        artist_name = 'Unknown Artist'

                    yield (track_name, artist_name)
                
            offset += limit
            pbar.update(len(items))

