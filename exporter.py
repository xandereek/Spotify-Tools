import json
import csv
import logging

def export_to_txt(file_name, tracks):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        count = 0
        for song in tracks:
            f.write(f"{song[0]} - {song[1]}\n")
            count += 1 
    logging.info("Saved %d tracks to %s.txt", count, file_name)

def export_to_json(file_name, tracks):
    with open(f"{file_name}.json", "w", encoding="utf-8") as f:
        
        track_list = [
            {"artist":artist_name, "track": track_name} for artist_name, track_name in tracks
        ]
        json.dump(track_list, f, indent=2)
    logging.info("Saved %d tracks to %s.json", len(track_list), file_name)

def export_to_csv(file_name, tracks):
    with open(f"{file_name}.csv", "w", newline="",  encoding="utf-8") as f:

        writer = csv.writer(f)
        writer.writerow(["Track", "Artist"])
        writer.writerows(tracks)

        logging.info("Saved tracks to %s.csv", file_name)

