import logging
import time
import requests
import auth
import fetcher
import exporter
import sys
import validation
import subprocess
import os
from spotipy import SpotifyException
from typing import Dict, Any, Optional
from constants import SourceOption

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_cpp_analyzer(playlist_name: str):
    print("\n--- Running Playlist Analysis ---")

    executable_name = "analyzer.exe" if sys.platform == "win32" else "analyzer"
    file_to_analyze = os.path.join("exports", f"{playlist_name}.json")

    if not os.path.exists(file_to_analyze):
        print(f"Error: Analysis requires {file_to_analyze}, but it was not found.")
        return
    
    command = [f"./{executable_name}", file_to_analyze]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except FileNotFoundError:
        print(f"Error: The '{executable_name}' program was not found in the project directory.")
        print("Please ensure you have compiled the C++ code.")
    except subprocess.CalledProcessError as e:
        print("Error: The C++ analysis failed.")
        print(e.stderr)

def main():
    max_retries = 3
    for retries in range(max_retries):
        try:
            sp = auth.get_spotify_client()
            logging.info("Successfully authenticated with Spotify.")
            break
        except (SpotifyException, requests.exceptions.RequestException) as e:
            logging.warning(f"Erorr authenticating with spotify. Attempt:{retries + 1}")
            if retries == max_retries - 1:
                logging.error(f"Failed to authenticate with spotify:{e}")
                sys.exit()
            time.sleep(1)

    wants_analysis_input = input("Analyze playlist for top artists? (y/n): ").lower()
    wants_analysis = wants_analysis_input.startswith('y')


    playlist_or_liked = validation.select_playlist_source()
    export_format = exporter.export_format()
    

    if playlist_or_liked == SourceOption.PLAYLIST.value:
        attempt = 0
        results: Optional[Dict[str, Any]] = None
        while attempt < max_retries:
            try:
                results = sp.current_user_playlists()
                break
            except (SpotifyException, requests.exceptions.RequestException):
                attempt += 1
                if attempt == max_retries:
                    logging.error("Failed to receive playlists.")
                    sys.exit(1)
                time.sleep(1)

        if results is None or 'items' not in results:
            logging.error("Failed to receive playlists or no playlists found.")
            sys.exit(1)

        print("\nPlaylists:")
        for index, playlist in enumerate(results['items']):
            print(f"{index+1}: {playlist['name']}")
        
        playlist_selection = -1
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
        tracks_generator = fetcher.playlist_fetcher(sp, playlist_id)

    elif playlist_or_liked == SourceOption.LIKED_SONGS.value:
        logging.info("User selected to export Liked Songs.")
        playlist_name = "liked songs"
        tracks_generator = fetcher.fetch_liked_songs(sp)

    exporters = {
            "1":exporter.export_to_txt,
            "2":exporter.export_to_json,
            "3":exporter.export_to_csv,
            "4":exporter.export_to_markdown
        }

    if not wants_analysis:
        print(f"\nExporting to selected format...")
        exporters[export_format](playlist_name, tracks_generator)
    else:
        print("Fetching tracks for analysis and export...")
        all_tracks = list(tracks_generator)

        print("\nExporting to JSON for analysis...")
        exporter.export_to_json(playlist_name, all_tracks)
        run_cpp_analyzer(playlist_name)

        if export_format == "2":
            print("\nUser-requested JSON export was already created for the analysis.")
        else:
            print(f"\nExporting to selected format...")
            exporters[export_format](playlist_name, all_tracks)

if __name__ == '__main__':
    main()
