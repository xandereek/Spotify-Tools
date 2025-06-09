import logging
from tqdm import tqdm

def playlist_fetcher(sp, playlist_id):
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
            pbar.len(items)
    
