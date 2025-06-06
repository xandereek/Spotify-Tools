import json
import csv

def export_to_txt(file_name, tracks):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        for song in tracks:
            f.write(song + "\n")
    print(f"Saved {len(tracks)} tracks to {file_name}.txt")

def export_to_json(file_name, tracks):
    with open(f"{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(tracks, f, indent=2)
    print(f"Saved {len(tracks)} tracks to {file_name}.json")

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
        print(f"Saved {len(tracks)} tracks to {file_name}.csv")
