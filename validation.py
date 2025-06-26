

def name_sanitizer(name):
        banned = r'\/:*?"<>|'
        new_name = ""
        for char in name:
            if char not in banned:
                new_name += char
        return new_name

def select_playlist_source():
    while True:
        try:
            playlist_or_liked = int(input("Playlists(1) or Liked songs(2)?: "))
            if playlist_or_liked in [1,2]:
                return playlist_or_liked
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")