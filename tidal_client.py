from typing import Dict, List

import tidalapi
from dotenv import find_dotenv, load_dotenv, set_key
from transliterate import translit


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
        self.session.load_oauth_session(
            self._token_type,
            self._access_token,
            self._refresh_token,
            self._expiry_time,
        )
        if not self.session.check_login:
            self.session.login_oauth_simple()

            dotenv_file = find_dotenv()
            load_dotenv(dotenv_file)

            set_key(dotenv_file, "TIDAL_TOKEN_TYPE", self.session.token_type)
            set_key(dotenv_file, "TIDAL_ACCESS_TOKEN", self.session.access_token)
            set_key(dotenv_file, "TIDAL_REFRESH_TOKEN", self.session.refresh_token)
            set_key(dotenv_file, "TIDAL_EXPIRY_TIME", str(self.session.expiry_time))

    def load_all_user_playlists(self) -> List[tidalapi.playlist.UserPlaylist]:
        return self.session.user.playlists()

    def load_playlist(
        self, playlist_name: str
    ) -> tidalapi.playlist.UserPlaylist | None:
        for playlist in self.load_all_user_playlists():
            if playlist.name == playlist_name:
                return playlist
        return None

    def delete_playlist(self, playlist_name: str):
        playlist = self.load_playlist(playlist_name)
        if playlist:
            playlist.delete()

    def create_playlist(self, playlist_name: str, playlist_desc: str, tids: List[str]):
        playlist = self.session.user.create_playlist(playlist_name, playlist_desc)
        playlist.add(tids)

    def get_search_query_result(self, text: str) -> List[tidalapi.Track]:
        res = self.session.search(text.lower())
        return res["tracks"]

    def process_search_query_result(
        self, result: List[tidalapi.Track], isrc: str, artist: str
    ) -> int | None:
        for t in result:
            if t.isrc == isrc:
                tidal_id = t.id
                return tidal_id

        # search in the query results
        possible_ids = list(
            filter(
                lambda s: artist in s.artist.name,
                result,
            )
        )
        if possible_ids:
            tidal_id = possible_ids[0].id
            return tidal_id

        return None

    def search_track(self, track: Dict) -> str | None:
        found_tracks = []
        found_tracks.extend(
            self.get_search_query_result(f"{track['artist']} {track['name']}")
        )
        found_tracks.extend(
            self.get_search_query_result(f"{track['name']} {track['artist']}")
        )

        tidal_id = self.process_search_query_result(
            found_tracks, track["isrc"], track["artist"]
        )
        if tidal_id:
            return tidal_id

        # for cases when tracks are transliterated (currently only Cyrillics to Latin)
        artist_ru = translit(track["artist"], "ru")

        found_tracks = []
        found_tracks.extend(
            self.get_search_query_result(f"{artist_ru} {track['name']}")
        )
        found_tracks.extend(
            self.get_search_query_result(f"{track['name']} {artist_ru}")
        )

        return self.process_search_query_result(found_tracks, track["isrc"], artist_ru)
