import logging
import time
import requests
import auth
import fetcher
import exporter
import sys
import validation
from spotipy import SpotifyException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


try:
    sp = auth.get_spotify_client()
    logging.info("Successfully authenticated with Spotify.")
except (SpotifyException, requests.exceptions.RequestException) as e:
    logging.error("Failed to authenticate with Spotify: %s", e)
    sys.exit(1)

max_retries = 3
attempt = 0

while attempt < max_retries:
    try:
        results = sp.current_user_playlists()
        break
    except (SpotifyException, requests.exceptions.RequestException) as e:
        attempt += 1
        if attempt == max_retries:
            logging.error("Failed to receive playlists.")
            sys.exit(1)
        time.sleep(1)

playlist_or_liked = validation.select_playlist_source()
        

if playlist_or_liked == 1:
    print("\nPlaylists:")
    for index, playlist in enumerate(results['items']):
        print(f"{index+1}: {playlist['name']}")
    
    while True:
        try:
            playlist_selection = int(input("\nSelect a playlist by number: ")) - 1
            if 0 <= playlist_selection < len(results['items']):
                break
            else:
                print(f"Please enter a number between 1 and {len(results['items'])}")
        except ValueError:
            print("Invalid Input. Please enter a number.")

    selected_playlist = results['items'][playlist_selection]
    playlist_id = selected_playlist['id']  
    playlist_name = validation.name_sanitizer(selected_playlist['name'])
    
    logging.info("User selected playlist: %s (ID: %s)", playlist_name, playlist_id)
    print(f"You selected: {playlist_name}\n")
    playlist_tracks = fetcher.playlist_fetcher(sp, playlist_id)

    export_format = exporter.export_format()
    
    exporters = {
        "1":exporter.export_to_txt,
        "2":exporter.export_to_json,
        "3":exporter.export_to_csv,
        "4":exporter.export_to_markdown
    }
    exporters[export_format](playlist_name, playlist_tracks)

elif playlist_or_liked == 2:
    logging.info("User selected to export Liked Songs.")
    playlist_name = "liked songs"

    export_format = exporter.export_format()

    liked_tracks = fetcher.fetch_liked_songs(sp)

    exporters = {
        "1":exporter.export_to_txt,
        "2":exporter.export_to_json,
        "3":exporter.export_to_csv,
        "4":exporter.export_to_markdown
    }
    exporters[export_format](playlist_name, liked_tracks)
