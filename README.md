# Spotify Playlist Exporter

A Python script to export your Spotify playlists and liked songs to various formats, and analyze them to find your top artists.

**Note**

This project is maintained as time allows. Additional features may be added down the road.

---

## Features

- Fetch tracks from your public and private playlists.
- Fetch your liked songs.
- **New!** Analyze any playlist to find your top 10 most frequent artists.
- Export track data (track name, artist name) to:
    - TXT files
    - JSON files
    - CSV files
    - Markdown files
- Displays progress bars during track fetching.
- Error handling (e.g., for network issues, API rate limits)
- Modular code structure for better maintainability
- User-friendly interface with clear prompts and progress indicators
- Restoring playlists (e.g., recreate from .txt or .csv backups) - *may be added in the future*

---

## Potential Future features    

- Restoring playlists (e.g., recreate from .txt or .csv backups)

---

## Setup

1.  **Clone the repository (or download the files).**

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Spotify API Credentials:**
    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create an app.
    - Note your `Client ID` and `Client Secret`.
    - In your app settings, set a `Redirect URI`. For local development, you can use `http://127.0.0.1:8888/callback`.
    - **Important:** The Redirect URI set in your Spotify Developer App settings must be an exact match to the `redirect_uri` value in your `config.json` file.
    - Edit the existing `config.json` file by replacing the placeholder values with your credentials. It should look like this:
      ```json
      {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "redirect_uri": "[http://127.0.0.1:8888/callback](http://127.0.0.1:8888/callback)"
      }
      ```
    - Alternatively, you can create a `config_local.json` file in the project root with the same structure. If this file exists, it will be used instead of `config.json`.

---

## A Note on the Analyzer

For convenience, this project includes a pre-compiled C++ analyzer for Windows (`analyzer.exe`). However, if you are on a different operating system (macOS, Linux) or feel safer compiling the code yourself, you can do so easily.

You will need a C++ compiler like `g++`. To compile, navigate to the project directory in your terminal and run:
```bash
g++ analyzer.cpp -o analyzer
```
This will create a new executable from the source code that you can run on your system.

---

## Usage

1.  **Run the main script:**
    ```bash
    python main.py
    ```
2.  The script will authenticate you with Spotify (this might open a browser window).
3.  Follow the on-screen prompts to:
    - Choose if you want to **analyze the playlist** for your top artists.
    - Choose whether to export from your playlists or your liked songs.
    - If exporting from playlists, select the playlist you want to export.
    - Choose the desired export format (TXT, JSON, CSV, or Markdown).
4.  The analysis (if requested) will be displayed in the terminal, and the exported file will be saved in the `exports/` directory.

**Note:** Playlist names containing Windows invalid characters (`\ / : * ? " < > |`) will have those characters removed from the exported file name.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
