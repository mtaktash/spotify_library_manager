# spotify_library_manager

## Setup
1. `pip install -r requirements.txt`
2. Get `client_id` and `client_secret` by creating an app on https://developer.spotify.com/. Set `redirect_uri` to something like `http://127.0.0.1:9090`
3. Create `.env` file with spotify details. The first run will also save tidal login details in `.env` file
```
SPOTIFY_CLIENT_ID=%client_id% 
SPOTIFY_CLIENT_SECRET=%client_secret%
SPOTIFY_REDIRECT_URI=%redirect_uri%
SPOTIFY_SCOPE="user-library-read"
```

## Scenarios
### Transfer one playlist:
- Run `python transfer_playlist_from_spotify_to_tidal.py -f "spotify playlist name" "tidal playlist name"`.
  - Pass `tidal playlist name` as an empty string `""` to create playlist name from spotify user name (or specified prefix) and spotify playlist name
  - Use `-f` option to rewrite playlist (deletes all playlists with this name)
  - Use `--prefix` to create custom playlist prefix, otherwise it'll use displayed spotify user name
  - Use `--save_missing` to save missing tracks in `logs/%save_missing_path%` as json
  - Use `--save_missing_path` to save missing tracks in `logs/%save_missing_path%` as json
### Transfer all logged user playlists
- Run `python transfer_all_playlists_from_spotify_to_tidal.py -f`
  - All arguments are the same
### Transfer playlists from a list
- Create a list of playlists, example list is in `playlists.txt` 
- It should contain spotify playlist links (for any playlist) or playlist names (but only for playlists created by the logged user)
- Run `bash transfer_playlists_list.sh playlists.txt`
- Missing tracks will be automatically saved

### Download tidal playlists
- Run `tidal-dl` to setup the downloader
- Run `bash download_tidal_playlists.sh %prefix%`
- `prefix` is the starting prefix for tidal playlists you want to download
  - Leave it empty to download all playlists
  - Write playlist name to download a single playlist
 
Was inspired by https://github.com/canta2899/spotify-to-tidal 

