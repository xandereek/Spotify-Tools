# Spotify Playlist Exporter

A Python script to export your Spotify playlists and liked songs to various formats (TXT, JSON, CSV).

## Features

- Fetch tracks from your public and private playlists.
- Fetch your liked songs.
- Export track data (track name, artist name) to:
    - TXT files
    - JSON files
    - CSV files
- Displays progress bars during track fetching.

## Setup

1.  **Clone the repository (or download the files).**
2.  **Install dependencies:**

    ```bash
    pip install spotipy tqdm
    ```
3.  **Set up Spotify API Credentials:**
    *   Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create an app.
    *   Note your `Client ID` and `Client Secret`.
    *   In your app settings (on the Spotify Developer Dashboard), set a `Redirect URI`. For local development, you can use `http://127.0.0.1:8888/callback`.
    *   Important: The Redirect URI set in your Spotify Developer App settings must be an exact match to the `redirect_uri` value in your `config.json` file.
    *   Edit the existing `config.json` file (located in the project root) by replacing the placeholder values with your actual `Client ID`, `Client Secret`, and `Redirect URI`.
    *   It should look like this:

        ```json
        {
          "client_id": "YOUR_CLIENT_ID",
          "client_secret": "YOUR_CLIENT_SECRET",
          "redirect_uri": "http://127.0.0.1:8888/callback"
        }
        ```
    *   Alternatively, you can create a `config_local.json` file in the project root with the same structure. If this file exists, it will be used instead of `config.json`. This is useful for local overrides and should be added to your `.gitignore` file if it contains sensitive information.

## Usage

1.  **Run the main script:**

    ```bash
    python main.py
    ```
2.  The script will authenticate you with Spotify (this might open a browser window for you to log in and authorize).
3.  Follow the on-screen prompts to:
    *   Choose whether to export from your playlists or your liked songs.
    *   If exporting from playlists, select the playlist you want to export.
    *   Choose the desired export format (TXT, JSON, or CSV).
5.  The exported file will be saved in the `exports/` directory (which will be created if it doesn't exist), named after the playlist (e.g., `exports/My Awesome Playlist.txt`) or `exports/liked songs.txt` for liked songs.

## Planned Features

- [ ] Error handling (e.g., for network issues, API rate limits)
- [ ] Usability improvements (e.g., clearer prompts, progress indicators)
- [ ] Restoring playlists (e.g., recreate from our .txt or .csv backups)
- [ ] Playlist analysis features (e.g., genre breakdown, pie chart of artists)

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
