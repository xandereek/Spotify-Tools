import logging

def playlist_fetcher(sp, playlist_id):
    logging.info("Fetching playlist tracks..")

    limit = 100
    offset = 0

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
             ##playlist_tracks.append(f"{track_name} - {artist_name}")
        offset += limit

def fetch_liked_songs(sp):
    logging.info("Fetching liked songs..")
    limit = 50
    offset = 0

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
            ## liked_tracks.append(f"{track_name} - {artist_name}")
        offset += limit
