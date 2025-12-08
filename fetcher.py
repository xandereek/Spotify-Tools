import logging
import requests
import time
from tqdm import tqdm
from spotipy import SpotifyException
from concurrent.futures import ThreadPoolExecutor



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
    all_tracks = []
    def get_page(offset):
        return retry_api_call(lambda: sp.playlist_tracks(playlist_id, limit=limit, offset=offset))
    
    offsets = range(0, total, limit)
    

    with tqdm(total=total, desc="Fetching Playlist", unit="track") as pbar:
         with ThreadPoolExecutor(max_workers=10) as executor:
              for response in executor.map(get_page, offsets):
                   items = response['items']
                   all_tracks.extend(items)
                   pbar.update(len(items))

    yield from loop_tracks(all_tracks)

def fetch_liked_songs(sp):
    """Fetches all liked songs using concurrent requests."""
    
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
    all_tracks = []
    
    def get_page(offset):
        return retry_api_call(lambda: sp.current_user_saved_tracks(limit=limit, offset=offset))
    
    offsets = range(0, total, limit)
    
    with tqdm(total=total, desc="Fetching liked songs", unit="track") as pbar:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for response in executor.map(get_page, offsets):
                items = response['items']
                all_tracks.extend(items)
                pbar.update(len(items))
    
    yield from loop_tracks(all_tracks)
