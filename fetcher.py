import logging
import requests
import time
from tqdm import tqdm
from spotipy import SpotifyException

def playlist_fetcher(sp, playlist_id):
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

