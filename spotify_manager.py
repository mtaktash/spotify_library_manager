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
