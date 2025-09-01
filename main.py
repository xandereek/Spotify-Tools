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
import threading
from queue import Queue, Empty
from spotipy import SpotifyException
from typing import Dict, Any, Optional, Iterable, Tuple
from constants import SourceOption

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def listen_to_process(proc, q):
    """Reads a process's stdout line by line and puts it into a queue."""
    try:
        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                q.put(line)
        for line in proc.stdout:
            q.put(line)
    except:
        pass
    finally:
        proc.stdout.close()

def run_cpp_analyzer(playlist_name: str):
    """Runs the C++ analyzer in a fully interactive session using Popen."""
    print("\nStarting Interactive Playlist Analysis")
    executable_name = "analyzer.exe" if sys.platform == "win32" else "analyzer"
    file_to_analyze = os.path.join("exports", f"{playlist_name}.json")
    
    if not os.path.exists(file_to_analyze):
        print(f"Error: Analysis requires {file_to_analyze}, but it was not found.")
        return

    command = [f"./{executable_name}", file_to_analyze]

    try:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=0
        )

        q = Queue()
        listener = threading.Thread(target=listen_to_process, args=(proc, q))
        listener.daemon = True
        listener.start()

        print("Connecting to analyzer...")
        
        time.sleep(0.5)
        
        while proc.poll() is None:
            try:
                output_found = False
                while True:
                    try:
                        line = q.get_nowait()
                        print(line, end='', flush=True)
                        output_found = True
                    except Empty:
                        break
                
                if output_found:
                    time.sleep(0.1)
                
                try:
                    user_input = input()
                except EOFError:
                    break
                    
                if proc.stdin:
                    proc.stdin.write(user_input + '\n')
                    proc.stdin.flush()

                if user_input.lower() == 'quit':
                    break
                    
                time.sleep(0.2)

            except (BrokenPipeError, KeyboardInterrupt):
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error during interaction: {e}")
                break
        
        try:
            while not q.empty():
                print(q.get_nowait(), end='', flush=True)
        except Empty:
            pass
            
        print("\nExiting interactive analysis")
        if proc.stdin:
            proc.stdin.close()
        proc.terminate()

        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        listener.join(timeout=2)

    except FileNotFoundError:
        print(f"Error: The '{executable_name}' program was not found.")
        print("Make sure to compile it first!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


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
        run_cpp_analyzer(playlist_name)

        if export_format == "2":
            print("\nUser-requested JSON export was already created for the analysis.")
        else:
            print(f"\nExporting {playlist_name} to selected format...")
            exporters[export_format](playlist_name, all_tracks)

if __name__ == '__main__':
    main()