import os
import json
import csv
import logging
import fetcher

export_dir = "exports"
os.makedirs(export_dir, exist_ok=True)

def export_format():
    while True:
            export_format = input("Export format? TXT(1), JSON(2), CSV(3), MARKDOWN(4): ")
            if export_format in ["1", "2", "3", "4"]:
                return export_format
            print("Invalid input. Please enter 1, 2, 3, or 4.")


def combine_playlist_tracks(sp, playlists_to_fetch:list):
    for playlist in playlists_to_fetch:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        print(f"\nFetching tracks from: {playlist_name}...")
        yield from fetcher.playlist_fetcher(sp, playlist_id)

def export_to_txt(file_name, tracks):

    """Exports a list of tracks to a plain text file.

    Each line in the file will be formatted as "Track Name - Artist Name".

    Args:
        file_name (str): The base name for the output file (without extension).
        tracks (iterable[tuple[str, str]]): An iterable of tuples, where each
                                             tuple contains a track name and an
                                             artist name.
    """

    path = os.path.join(export_dir, f"{file_name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        count = 0
        for song in tracks:
            f.write(f"{song[0]} - {song[1]}\n")
            count += 1 
    logging.info("Saved %d tracks to %s.txt", count, file_name)

def export_to_json(file_name, tracks):

    """Exports a list of tracks to a JSON file.

    The JSON file will contain a list of objects, with each object
    representing a track with "artist" and "track" keys.

    Args:
        file_name (str): The base name for the output file (without extension).
        tracks (iterable[tuple[str, str]]): An iterable of tuples, where each
                                             tuple contains a track name and an
                                             artist name.
    """

    path = os.path.join(export_dir, f"{file_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        
        # This is a shortcut to reformat our simple list of tracks.
        # It creates a new list where each song is structured with "track" and "artist" labels.
        track_list = [
            {"track": track_name, "artist":artist_name} for track_name, artist_name in tracks
        ]
        # This writes the structured list to the file. 
        # The "indent=2" part makes the file nicely formatted and easy for humans to read.
        json.dump(track_list, f, indent=2)

    logging.info("Saved %d tracks to %s.json", len(track_list), file_name)

def export_to_csv(file_name, tracks):

    """Exports a list of tracks to a CSV file.

    The CSV will have two columns: "Track" and "Artist".

    Args:
        file_name (str): The base name for the output file (without extension).
        tracks (iterable[tuple[str, str]]): An iterable of tuples, where each
                                             tuple contains a track name and an
                                             artist name.
    """
    
    path = os.path.join(export_dir, f"{file_name}.csv")
    # We add newline="" to prevent blank rows from appearing in the saved CSV file.
    with open(path, "w", newline="",  encoding="utf-8") as f:

        # This sets up a "writer" that knows how to properly format data for a CSV file.
        writer = csv.writer(f)
        # ".writerow" writes a single row. We use it here for the column headers.
        writer.writerow(["Track", "Artist"])
        # ".writerows" writes all the items from our track list at once.
        writer.writerows(tracks)

        logging.info("Saved tracks to %s.csv", file_name)

def export_to_markdown(file_name, tracks):
    count = 0
    path = os.path.join(export_dir, f"{file_name}.md")
    with open(path, "w", encoding="utf-8") as f:
        """Exports a list of tracks to a Markdown-formatted table.

        The Markdown file includes a header and a table with two columns: "Track Name" and "Artist".

        Args:
            file_name (str): The base name for the output file (without extension).
            tracks (iterable[tuple[str, str]]): An iterable of tuples, where each
                                                tuple contains a track name and an
                                                artist name.
        """
        count = 0

        # These lines write the specific text required to create a Markdown table.
        # '#' is a main header, and the '|' and '---' characters define the table structure.
        f.write(f"# Playlist: {file_name}\n\n")
        f.write("| Track Name | Artist |\n")
        f.write("|------------|--------|\n")
        
        # This for-loop unpacks each tuple from the 'tracks' generator
        # into two separate variables, 'track_name' and 'artist_name', for each iteration.
        for track_name, artist_name in tracks:
            f.write(f"| {track_name} | {artist_name} |\n")
            count += 1
        logging.info("Saved %d tracks to %s.md", count, file_name)

