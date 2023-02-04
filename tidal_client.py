from typing import Dict, List

import tidalapi
from dotenv import find_dotenv, load_dotenv, set_key


class TidalClient:
    def __init__(
        self, token_type: str, access_token: str, refresh_token: str, expiry_time: str
    ):
        self.session: tidalapi.Session = tidalapi.Session()
        self._token_type: str = token_type
        self._access_token: str = access_token
        self._refresh_token: str = refresh_token
        self._expiry_time: str = expiry_time

    def login(self):
        if (
            self._token_type
            and self._access_token
            and self._refresh_token
            and self._expiry_time
        ):
            self.session.load_oauth_session(
                self._token_type,
                self._access_token,
                self._refresh_token,
                self._expiry_time,
            )
        else:
            self.session.login_oauth_simple()

            dotenv_file = find_dotenv()
            load_dotenv(dotenv_file)

            set_key(dotenv_file, "TIDAL_TOKEN_TYPE", self.session.token_type)
            set_key(dotenv_file, "TIDAL_ACCESS_TOKEN", self.session.access_token)
            set_key(dotenv_file, "TIDAL_REFRESH_TOKEN", self.session.refresh_token)
            set_key(dotenv_file, "TIDAL_EXPIRY_TIME", str(self.session.expiry_time))

    def search_track(self, track: Dict):
        found_tracks = []
        tidal_id = None

        # search artist name
        query = f"{track['artist']} {track['name']}"
        query = query.lower()
        res = self.session.search(query)
        found_tracks.extend(res["tracks"])

        # search name artist
        query = f"{track['name']} {track['artist']}"
        query = query.lower()
        res = self.session.search(query)
        found_tracks.extend(res["tracks"])

        try:
            for t in found_tracks:
                if t.isrc == track["isrc"]:
                    tidal_id = t.id
                    break
            if not tidal_id:
                possible_ids = filter(
                    lambda s: track["artist"] in s.artist.name, res["tracks"]
                )
                tidal_id = list(possible_ids)[0].id
        except Exception:
            pass

        return tidal_id

    def add_to_playlist(self, playlist_name: str, tids: List[str]):
        playlist = self.session.user.create_playlist(
            playlist_name, "Songs saved from spotify"
        )
        playlist.add(tids)
