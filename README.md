# Spotify Playlist Exporter

A Python script to export your Spotify playlists and liked songs to various formats (TXT, JSON, CSV).

## Features

- Fetch tracks from your public and private playlists.
- Fetch your liked songs.
- Export track data (track name, artist name) to:
    - TXT files
    - JSON files
    - CSV files

## Setup

1.  **Clone the repository (or download the files).**
2.  **Install dependencies:**

    ```bash
    pip install spotipy tqdm
    ```
4.  **Set up Spotify API Credentials:**
    *   Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create an app.
    *   Note your `Client ID` and `Client Secret`.
    *   In your app settings (on the Spotify Developer Dashboard), set a `Redirect URI`. A common one for local development is `http://localhost:8888/callback`.
    *   Create a file named `secrets_1.py` in the same directory as the script and add your credentials like this:

        ```python
        CLIENT_ID = "YOUR_CLIENT_ID"
        CLIENT_SECRET = "YOUR_CLIENT_SECRET"
        REDIRECT_URI = "YOUR_REDIRECT_URI" # e.g., "http://localhost:8888/callback"
        ```

## Usage

1.  **Run the main script:**

    ```bash
    python main.py
    ```
3.  The script will authenticate you with Spotify (this might open a browser window for you to log in and authorize).
4.  Follow the on-screen prompts to:
    *   Choose whether to export from your playlists or your liked songs.
    *   If exporting from playlists, select the playlist you want to export.
    *   Choose the desired export format (TXT, JSON, or CSV).
5.  The exported file will be saved in the same directory as the script, named after the playlist (e.g., `My Awesome Playlist.txt`) or `liked songs.txt` for liked songs.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is currently unlicensed. Feel free to use it as you wish. (Consider adding an MIT License if distributing).
