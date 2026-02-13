from slugify import slugify

def name_sanitizer(name):
        banned = r'\/:*?"<>|'
        new_name = ""
        for char in name:
            if char not in banned:
                new_name += char

        if not new_name.strip():
            return "playlist"
        
        return slugify(new_name.strip())

def select_playlist_source():
    while True:
        try:
            playlist_or_liked = int(input("Playlists(1) or Liked songs(2)? or Albums(3): "))
            if playlist_or_liked in [1,2,3]:
                return playlist_or_liked
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_playlists(available_playlists):
    num_playlists = len(available_playlists)
    while True:
        try:
            raw_input = input(f"\nSelect one or more playlists by number (e.g., 1, 3, 5): ")
            string_numbers = raw_input.split(',')
            selected_indices = [int(i.strip()) - 1 for i in string_numbers]

            if all(0 <= i < num_playlists for i in selected_indices):
                return [available_playlists[i] for i in selected_indices]
            else:
                print(f"Error: Please enter numbers between 1 and {num_playlists}.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")