

def playlist_fetcher(sp, playlist_id):
    print("Gettings tracks...")

    playlist_tracks = [] 
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
            playlist_tracks.append(f"{track_name} - {artist_name}")
        
        offset += limit
    return playlist_tracks
def fetch_liked_songs(sp):
    print("Gettings tracks...")

    liked_tracks = []
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
            liked_tracks.append(f"{track_name} - {artist_name}")
        
        offset += limit
    return liked_tracks
