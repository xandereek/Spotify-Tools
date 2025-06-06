import spotipy
import auth
import fetcher

sp = auth.get_spotify_client()

def create_file(file_name, tracks):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        for song in tracks:
            f.write(song + "\n")
    print(f"Saved {len(tracks)} tracks to {file_name}.txt")



results = sp.current_user_playlists()

playlist_or_liked = int(input("Playlists(1) or Liked songs(2)?: "))

if playlist_or_liked == 1:
    print("\nPlaylists:")
    for index, playlist in enumerate(results['items']):
        print(f"{index+1}: {playlist['name']} PLaylist ID:{playlist['id']}")
    
    playlist_selection = int(input("\nSelect a playlist by number: ")) - 1
    selected_playlist = results['items'][playlist_selection]
    playlist_id = selected_playlist['id']
    playlist_name = selected_playlist['name']

    print(f"You selected: {playlist_name} ID: {playlist_id}\n")
    playlist_tracks = fetcher.playlist_fetcher(sp, playlist_id)

    create_file(playlist_name, playlist_tracks)

elif playlist_or_liked == 2:
    liked_tracks = fetcher.fetch_liked_songs(sp)
    create_file("liked songs", liked_tracks)

    

