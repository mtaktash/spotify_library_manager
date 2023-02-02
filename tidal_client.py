import re
import tidalapi
from typing import Any, List


class TidalClient:
    def __init__(self):
        self.session: tidalapi.Session = tidalapi.Session()

    def login(self):
        self.session.login_oauth_simple()

    @staticmethod
    def __normalize(query: str) -> str:
        normalized = "".join(
            filter(lambda character: ord(character) < 0xFF, query.lower())
        )
        normalized = (
            query.split("-")[0].strip().split("(")[0].strip().split("[")[0].strip()
        )
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def search_track(self, track) -> str | None:
        query = self.__normalize(f"{track['name']} {track['artist']}")
        res = self.session.search(query)
        tidal_id = None
        try:
            for t in res["tracks"]:
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
