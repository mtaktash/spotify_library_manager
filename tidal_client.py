from typing import Dict, List

import dateutil
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
        try:
            self.session.load_oauth_session(
                self._token_type,
                self._access_token,
                self._refresh_token,
                self._expiry_time,
            )
            assert self.session.check_login()

        except Exception:
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
        query_size = 300
        playlist = self.session.user.create_playlist(playlist_name, playlist_desc)
        for i in range(0, len(tids), query_size):
            playlist.add(tids[i : i + query_size])

    def _artist_name_search_query_result(
        self, artist: str, name: str, isrc: str
    ) -> int | None:
        result = self.session.search(f"{artist} {name}")["tracks"]
        result.extend(self.session.search(f"{name} {artist}")["tracks"])

        for t in result:
            if t.isrc == isrc:
                tidal_id = t.id
                return tidal_id

        # search in the query results
        possible_tracks = list(
            filter(
                lambda s: artist in s.artist.name,
                result,
            )
        )
        if possible_tracks:
            tidal_id = possible_tracks[0].id
            return tidal_id

        return None

    def _name_album_date_search_query_result(
        self, album: str, release_date: str, isrc: str
    ) -> int | None:
        release_date = dateutil.parser.parse(release_date)

        result = self.session.search(album)["albums"]
        possible_tracks = list()
        for album in result:
            # get the release date if it’s available
            # otherwise get the day it was released on TIDAL to not raise an error
            if album.year == release_date.year:
                possible_tracks.extend(album.tracks())

        # album artist and name might differ from spotify one
        # thus try a search by id only
        for t in possible_tracks:
            if t.isrc == isrc:
                tidal_id = t.id
                return tidal_id

        return None

    def search_track(self, track: Dict) -> str | None:
        # search artist name first
        tidal_id = self._artist_name_search_query_result(
            track["artist"],
            track["name"],
            track["isrc"],
        )
        if tidal_id:
            return tidal_id

        # for cases when tracks are transliterated (currently only Cyrillics to Latin)
        artist_ru = translit(track["artist"], "ru")

        tidal_id = self._artist_name_search_query_result(
            artist_ru,
            track["name"],
            track["isrc"],
        )

        if tidal_id:
            return tidal_id

        # search by album without track name
        tidal_id = self._name_album_date_search_query_result(
            track["album"], track["album_release_date"], track["isrc"]
        )

        return tidal_id
