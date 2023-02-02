import re
import tidalapi
from typing import Dict, List
from pprint import pprint


class TidalClient:
    def __init__(self):
        self.session: tidalapi.Session = tidalapi.Session()

    def login(self):
        self.session.login_oauth_simple()

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
        except Exception as e:
            pass

        return tidal_id

    def add_to_playlist(self, playlist_name: str, tids: List[str]):
        playlist = self.session.user.create_playlist(
            playlist_name, "Songs saved from spotify"
        )
        playlist.add(tids)
