# spotify_library_manager

1. `pip install -r requirements.txt`
2. Get `client_id` and `client_secret` by creating an app on https://developer.spotify.com/. Set redirect uri to something like http://127.0.0.1:9090
3. Create `.env` file with 
```
SPOTIFY_CLIENT_ID=%client_id% 
SPOTIFY_CLIENT_SECRET=%client_secret%
SPOTIFY_REDIRECT_URI=%redirect_uri%
SPOTIFY_SCOPE="user-library-read"
```

4. `python main.py "spotify playlist name" "tidal playlist name"`


Heavily inspired by https://github.com/canta2899/spotify-to-tidal 
