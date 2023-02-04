from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    """Class that manages Spotify library"""

    def __init__(
        self, client_id: str, client_secret: str, redirect_uri: str, scope: str
    ):
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_uri: str = redirect_uri
        self._scope: str = scope
        self.sp: spotipy.Spotify

    def login(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self._client_id,
                client_secret=self._client_secret,
                redirect_uri=self._redirect_uri,
                scope=self._scope,
            )
        )

    def get_user_name(self):
        return self.sp.current_user()["display_name"]

    def load_all_user_playlists(self) -> List[Dict]:
        all_items = []
        playlists = self.sp.current_user_playlists()
        while playlists:
            all_items.extend(playlists["items"])
            if playlists["next"]:
                playlists = self.sp.next(playlists)
            else:
                playlists = None
        return all_items

    def load_playlist(self, playlist_name: str) -> Dict | None:
        for playlist in self.load_all_user_playlists():
            if playlist["name"] == playlist_name:
                return playlist
        return None

    def load_playlist_tracks(self, playlist_name: str):
        playlist_info = self.load_playlist(playlist_name)
        playlist_id = playlist_info["id"]

        all_items = []
        tracks = self.sp.playlist_tracks(playlist_id)
        while tracks:
            all_items.extend(tracks["items"])
            if tracks["next"]:
                tracks = self.sp.next(tracks)
            else:
                tracks = None
        return all_items
