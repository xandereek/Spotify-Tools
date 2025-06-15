import logging
from tqdm import tqdm

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

    logging.info("Fetching playlist tracks..")

    response = sp.playlist_tracks(playlist_id, limit=1)
    total = response.get('total', 0)

    limit = 100
    offset = 0

    with tqdm(total=total, desc="Fetching Playlist", unit="track") as pbar:
        while True:
            response = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
            items = response['items']

            if not items:
                break

            for i in items:
                track = i['track']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
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
            response = sp.current_user_saved_tracks(limit=limit, offset=offset)
            items = response['items']

            if not items:
                break

            for i in items:
                track = i['track']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                
                yield (track_name, artist_name)
            offset += limit
            pbar.update(len(items))
    
