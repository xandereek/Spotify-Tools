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
from queue import Queue, Empty
from spotipy import SpotifyException
from typing import Dict, Any, Optional, Iterable, Tuple
from constants import SourceOption

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


library_path = os.path.join(os.getcwd(), "analyzer.dll")
library = ctypes.CDLL(library_path)

library.display_top_10_artists.argtypes = [ctypes.c_char_p]
library.display_top_10_artists.restype = None

logging.info("Succesfully loaded DLL.")

def cpp_integration(filename):
    json_filename = os.path.join("exports", f"{filename}.json")

    library.display_top_10_artists(json_filename.encode('utf-8'))

def main():
    max_retries = 3
    sp = None
    for retries in range(max_retries):
        try:
            sp = auth.get_spotify_client()
            logging.info("Successfully authenticated with Spotify.")
            break
        except (SpotifyException, requests.exceptions.RequestException) as e:
            logging.warning(f"Error authenticating with spotify. Attempt:{retries + 1}")
            if retries == max_retries - 1:
                logging.error(f"Failed to authenticate with spotify:{e}")
                sys.exit()
            time.sleep(1)
    
    if sp is None:
        logging.error("Could not create a Spotify client.")
        sys.exit(1)

    wants_analysis_input = input("Analyze playlist for top artists? (y/n): ").lower()
    wants_analysis = wants_analysis_input.startswith('y')

    playlist_or_liked = validation.select_playlist_source()
    export_format = exporter.export_format()
    
    tracks_generator: Optional[Iterable[Tuple[str, str]]] = None
    playlist_name = ""

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

        available_playlists = results['items']
        print("\nYour Playlists:")
        for index, playlist in enumerate(available_playlists):
            print(f"{index+1}: {playlist['name']}")
        
        selected_playlists = validation.select_playlists(available_playlists)

        if len(selected_playlists) == 1:
            playlist = selected_playlists[0]
            playlist_name = validation.name_sanitizer(playlist['name'])
            tracks_generator = fetcher.playlist_fetcher(sp, playlist['id'])
            print(f"You selected: {playlist['name']}\n")
        else:
            print(f"\nCombining {len(selected_playlists)} playlists.")
            playlist_name_input = input("Please enter a name for the combined export file: ")
            playlist_name = validation.name_sanitizer(playlist_name_input)
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
        exporters[export_format](playlist_name, tracks_generator)
    else:
        print("\nFetching tracks for analysis and export...")
        all_tracks = list(tracks_generator)

        print("\nExporting to JSON for analysis...")
        exporter.export_to_json(playlist_name, all_tracks)

        cpp_integration(playlist_name)

        if export_format == "2":
            print("\nUser-requested JSON export was already created for the analysis.")
        else:
            print(f"\nExporting {playlist_name} to selected format...")
            exporters[export_format](playlist_name, all_tracks)

if __name__ == '__main__':
    main()