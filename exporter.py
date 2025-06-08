import json
import csv
import logging

def export_to_txt(file_name, tracks):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        for song in tracks:
            f.write(song + "\n")
    logging.info("Saved %d tracks to %s.txt", len(tracks), file_name)

def export_to_json(file_name, tracks):
    with open(f"{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(tracks, f, indent=2)
    logging.info("Saved %d tracks to %s.json", len(tracks), file_name)

def export_to_csv(file_name, tracks):
    with open(f"{file_name}.csv", "w", newline="",  encoding="utf-8") as f: 
        writer = csv.writer(f)
        writer.writerow(["Track", "Artist"])
        for track in tracks:
            try:
                track_name, artist_name = track.split(" - ", 1)
            except ValueError:
                    track_name, artist_name = track, ""
            
            writer.writerow([track_name, artist_name])
        logging.info("Saved %d tracks to %s.csv", len(tracks), file_name)

