# spotify_library_manager

1. `pip install -r requirements.txt`
2. Get `client_id` and `client_secret` by creating an app on https://developer.spotify.com/. Set `redirect_uri` to something like `http://127.0.0.1:9090`
3. Create `.env` file with 
```
SPOTIFY_CLIENT_ID=%client_id% 
SPOTIFY_CLIENT_SECRET=%client_secret%
SPOTIFY_REDIRECT_URI=%redirect_uri%
SPOTIFY_SCOPE="user-library-read"
```

The first run will save tidal login details in `.env` file

4. Transfer one playlist:
  - Run `python transfer_playlist_from_spotify_to_tidal.py -f "spotify playlist name" "tidal playlist name"`. 
  - Use `-f` option to rewrite playlist (deletes all playlists with this name)
5. Transfer all user playlists
  - Run `python transfer_all_playlists_from_spotify_to_tidal.py -f`
  - Use `-f` option to rewrite playlist (deletes all playlists with this name)
  - Use `--prefix` to create custom name, otherwise it'll use displayed spotify user name
  - Use `--save_missing` to save missing tracks in `logs/` as json
  
Was inspired by https://github.com/canta2899/spotify-to-tidal 
