import logging
import requests
import time
from tqdm import tqdm
from spotipy import SpotifyException



def retry_api_call(func) -> dict: # type: ignore
    max_retries = 3

    for attempt in range(max_retries):
        try:
            return func()
        except (SpotifyException, requests.exceptions.RequestException) as e:  
                    logging.warning(f"Error getting tracks Attempt{attempt}: {e}")
                    if attempt  == max_retries - 1:
                        logging.error("Failed getting tracks")
                        raise e
                    logging.warning(f"Error getting tracks Attempt {attempt + 1}: {e}")
                    time.sleep(1)

def loop_tracks(items):
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
            try:
                response = retry_api_call(lambda: sp.playlist_tracks(playlist_id, limit=limit, offset=offset))
                items = response['items']
            except (SpotifyException, requests.exceptions.RequestException) as e:
                logging.error("Failed getting tracks after retries")
                break 

            if not items:
                break

            yield from loop_tracks(items)
            
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
    
    try:
        response = sp.current_user_saved_tracks(limit=1)
        total = response.get('total', 0)
    except (SpotifyException, requests.exceptions.RequestException) as e:
        logging.error(f"Error fetching liked songs data: {e}")
        return
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return

    limit = 50
    offset = 0
    
    with tqdm(total=total, desc="Fetching liked songs", unit="track") as pbar:
        while True:
            try:
                response = retry_api_call(lambda: sp.current_user_saved_tracks(limit=limit, offset=offset))
                items = response['items']
            except (SpotifyException, requests.exceptions.RequestException) as e:
                logging.error("Failed getting liked songs after retries")
                break

            if not items:
                break

            yield from loop_tracks(items)
                
            offset += limit
            pbar.update(len(items))

