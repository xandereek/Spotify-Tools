import logging
import time
import requests
import auth
import fetcher
import exporter
import sys
import validation
import ctypes
import os
from spotipy import SpotifyException
from typing import Dict, Any, Optional, Iterable, Tuple
from constants import SourceOption

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler('logs/spotify-tools.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

library_path = os.path.join(os.getcwd(), "analyzer.dll")
library = ctypes.CDLL(library_path)

library.display_top_10_artists.argtypes = [ctypes.c_char_p]
library.display_top_10_artists.restype = None

logging.info("Successfully loaded DLL.")

def cpp_integration(filename):
    json_filename = os.path.join("exports", f"{filename}.json")
    logging.info(f"Starting C++ analysis for: {filename}")
    library.display_top_10_artists(json_filename.encode('utf-8'))
    logging.info("C++ analysis completed")

def main():
    max_retries = 3
    sp = None
    logging.info("Starting application")

    for retries in range(max_retries):
        try:
            sp = auth.get_spotify_client()
            logging.info("Successfully authenticated with Spotify.")
            break
        except (SpotifyException, requests.exceptions.RequestException) as e:
            logging.warning(f"Error authenticating with spotify. Attempt:{retries + 1}")
            if retries == max_retries - 1:
                logging.error(f"Failed to authenticate with spotify:{e}")
                sys.exit(1)
            time.sleep(1)
    
    if sp is None:
        logging.error("Could not create a Spotify client.")
        sys.exit(1)

    wants_analysis_input = input("Analyze playlist for top artists? (y/n): ").lower()
    wants_analysis = wants_analysis_input.startswith('y')

    logging.info(f"User wants analysis: {wants_analysis}")

    playlist_or_liked = validation.select_playlist_source()
    logging.info(f"User selected source: {playlist_or_liked}")
    
    export_format = exporter.export_format()
    logging.info(f"User selected export format: {export_format}")

    tracks_generator: Optional[Iterable[Tuple[str, str]]] = None
    playlist_name = ""

    if playlist_or_liked == SourceOption.PLAYLIST.value:
        attempt = 0
        results: Optional[Dict[str, Any]] = None
        while attempt < max_retries:
            try:
                results = sp.current_user_playlists()
                logging.info(f"Successfully fetched user playlists")
                break
            except (SpotifyException, requests.exceptions.RequestException):
                attempt += 1
                logging.warning(f"Failed to fetch playlists, attempt {attempt}/{max_retries}")
                if attempt == max_retries:
                    logging.error("Failed to receive playlists.")
                    sys.exit(1)
                time.sleep(1)

        if results is None or 'items' not in results:
            logging.error("Failed to receive playlists or no playlists found.")
            sys.exit(1)

        available_playlists = results['items']
        print("\nYour Playlists:")
        for index, playlist in enumerate(available_playlists):
            print(f"{index+1}: {playlist['name']}")
        
        selected_playlists = validation.select_playlists(available_playlists)
        logging.info(f"User selected {len(selected_playlists)} playlist(s)")

        if len(selected_playlists) == 1:
            playlist = selected_playlists[0]
            playlist_name = validation.name_sanitizer(playlist['name'])
            logging.info(f"Fetching tracks from playlist: {playlist['name']}")
            tracks_generator = fetcher.playlist_fetcher(sp, playlist['id'])
            print(f"You selected: {playlist['name']}\n")
        else:
            print(f"\nCombining {len(selected_playlists)} playlists.")
            logging.info("Combining multiple playlists")
            playlist_name_input = input("Please enter a name for the combined export file: ")
            playlist_name = validation.name_sanitizer(playlist_name_input)
            logging.info(f"Combined playlist name: {playlist_name}")
            tracks_generator = exporter.combine_playlist_tracks(sp,  selected_playlists)

    elif playlist_or_liked == SourceOption.LIKED_SONGS.value:
        logging.info("User selected to export Liked Songs.")
        playlist_name = "liked songs"
        tracks_generator = fetcher.fetch_liked_songs(sp)

    if not tracks_generator:
        logging.error("Could not fetch any tracks.")
        sys.exit(1)

    exporters = {
        "1": exporter.export_to_txt,
        "2": exporter.export_to_json,
        "3": exporter.export_to_csv,
        "4": exporter.export_to_markdown
    }

    if not wants_analysis:
        print(f"\nExporting {playlist_name} to selected format...")
        logging.info(f"Starting export of {playlist_name}")
        exporters[export_format](playlist_name, tracks_generator)
        logging.info("Export completed successfully")
    else:
        print("\nFetching tracks for analysis and export...")
        logging.info("Converting generator to list for analysis")
        all_tracks = list(tracks_generator)
        logging.info(f"Fetched {len(all_tracks)} tracks")

        print("\nExporting to JSON for analysis...")
        exporter.export_to_json(playlist_name, all_tracks)

        cpp_integration(playlist_name)

        if export_format == "2":
            print("\nUser-requested JSON export was already created for the analysis.")
            logging.info("Skipping duplicate JSON export")
        else:
            print(f"\nExporting {playlist_name} to selected format...")
            logging.info(f"Creating additional export in format {export_format}")
            exporters[export_format](playlist_name, all_tracks)
            logging.info("Additional export completed")
    
    logging.info("Application completed with no errors")

if __name__ == '__main__':
    main()