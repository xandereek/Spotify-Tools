import spotipy
import auth
import fetcher
import exporter

sp = auth.get_spotify_client()





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
    export_format = input("Export format? TXT(1), JSON(2), CSV(3): ")
    if export_format == "1":
        exporter.export_to_txt(playlist_name, playlist_tracks)
    elif export_format == "2":
        exporter.export_to_json(playlist_name, playlist_tracks)
    elif export_format == "3":
        exporter.export_to_csv(playlist_name, playlist_tracks)
    else:
        print("Invalid format selected. Defaulting to TXT.")
        exporter.export_to_txt(playlist_name, playlist_tracks)

elif playlist_or_liked == 2:
    export_format = input("Export format? TXT(1), JSON(2), CSV(3): ")
    liked_tracks = fetcher.fetch_liked_songs(sp)
    if export_format == "1":
        exporter.export_to_txt("liked songs", liked_tracks)
    elif export_format == "2":
        exporter.export_to_json("liked songs", liked_tracks)
    elif export_format == "3":
        exporter.export_to_csv("liked songs", liked_tracks)
    else:
        print("Invalid format selected. Defaulting to TXT.")
        exporter.export_to_txt("liked songs", liked_tracks)

    

