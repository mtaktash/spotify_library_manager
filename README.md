# spotify_library_manager

## Setup
1. `pip install -r requirements.txt`
2. Get `client_id` and `client_secret` by **creating an app** on https://developer.spotify.com/dashboard
3. Set `redirect_uri` in **app settings** (go to an app in https://developer.spotify.com/dashboard -> edit settings -> redirect uri) to something like `http://127.0.0.1:9090`
4. Create `.env` file with spotify details. 
```
SPOTIFY_CLIENT_ID=%client_id% 
SPOTIFY_CLIENT_SECRET=%client_secret%
SPOTIFY_REDIRECT_URI=%redirect_uri%
SPOTIFY_SCOPE="user-library-read"
```
5. The first run **ask to login to tidal** and save tidal login details in `.env` file
6. You need to have a paid tidal account

## Scenarios
### spotify to tidal
#### transfer one playlist
- Run `python transfer_playlist_from_spotify_to_tidal.py -f "spotify playlist name" "tidal playlist name"`.
  - Use `-f` option to rewrite tidal playlist (deletes all playlists with this name)
  - Use `--prefix` to create custom playlist prefix (if "tidal playlist name" is empty), otherwise the script will use displayed spotify user name
  - Use `--save_missing` to save missing tracks as a json
  - Use `--save_missing_path` to specify the file where the json with missing tracks will be saved. If empty, the default path (`logs/missing_{datetime.datetime.now()}.json`) will be used
  - Pass `tidal playlist name` as an empty string `""` to create playlist name from spotify username (or `prefix` if it exists) and spotify playlist name

#### transfer all logged user playlists
- Run `python transfer_all_user_playlists_from_spotify_to_tidal.py -f`
  - All arguments are the same
  
#### transfer playlists from a list
- Create a list of playlists, example list is in `playlists.txt` 
- It should contain spotify playlist links (for any playlist) or playlist names (but only for playlists created by the logged user)
- Run `bash transfer_playlists_list.sh playlists.txt`
- Missing tracks will be automatically saved

### download 
#### tidal playlists
- Run `tidal-dl` to setup the downloader
- Run `bash download_tidal_playlists.sh %prefix%`
- `prefix` is the starting prefix for tidal playlists you want to download
  - Leave it empty to download all playlists
  - Write playlist name to download a single playlist
 
Was inspired by https://github.com/canta2899/spotify-to-tidal 

