import os
import json
import csv
import logging

export_dir = "exports"
os.makedirs(export_dir, exist_ok=True)


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
        
        track_list = [
            {"track": track_name, "artist":artist_name} for track_name, artist_name in tracks
        ]
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
    with open(path, "w", newline="",  encoding="utf-8") as f:

        writer = csv.writer(f)
        writer.writerow(["Track", "Artist"])
        writer.writerows(tracks)

        logging.info("Saved tracks to %s.csv", file_name)

