import logging
import auth
import fetcher
import exporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

sp = auth.get_spotify_client()
logging.info("Successfully authenticated with Spotify.")

results = sp.current_user_playlists()

playlist_or_liked = int(input("Playlists(1) or Liked songs(2)?: "))

if playlist_or_liked == 1:
    print("\nPlaylists:")
    for index, playlist in enumerate(results['items']):
        print(f"{index+1}: {playlist['name']}")
    
    playlist_selection = int(input("\nSelect a playlist by number: ")) - 1
    selected_playlist = results['items'][playlist_selection]
    playlist_id = selected_playlist['id']
    playlist_name = selected_playlist['name']
    
    logging.info("User selected playlist: %s (ID: %s)", playlist_name, playlist_id)
    print(f"You selected: {playlist_name}\n")

    playlist_tracks = fetcher.playlist_fetcher(sp, playlist_id)
    export_format = input("Export format? TXT(1), JSON(2), CSV(3): ")
    if export_format == "1":
        exporter.export_to_txt(playlist_name, playlist_tracks)
    elif export_format == "2":
        exporter.export_to_json(playlist_name, playlist_tracks)
    elif export_format == "3":
        exporter.export_to_csv(playlist_name, playlist_tracks)
    else:
        logging.warning("User selected an invalid export format. Defaulting to TXT.")
        print("Invalid format selected. Defaulting to TXT.")
        exporter.export_to_txt(playlist_name, playlist_tracks)

elif playlist_or_liked == 2:
    logging.info("User selected to export Liked Songs.")
    export_format = input("Export format? TXT(1), JSON(2), CSV(3): ")
    liked_tracks = fetcher.fetch_liked_songs(sp)
    if export_format == "1":
        exporter.export_to_txt("liked songs", liked_tracks)
    elif export_format == "2":
        exporter.export_to_json("liked songs", liked_tracks)
    elif export_format == "3":
        exporter.export_to_csv("liked songs", liked_tracks)
    else:
        logging.warning("User selected an invalid export format. Defaulting to TXT.")
        print("Invalid format selected. Defaulting to TXT.")
        exporter.export_to_txt("liked songs", liked_tracks)
