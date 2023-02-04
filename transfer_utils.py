import datetime
from typing import Dict, List

from tqdm import tqdm

from spotify_client import SpotifyClient
from tidal_client import TidalClient


def parse_spotify_tracks(tracks: List):
    return [
        dict(
            name=item["track"]["name"],
            artist=item["track"]["artists"][0]["name"],
            album=item["track"]["album"]["name"],
            isrc=item["track"]["external_ids"]["isrc"],
        )
        for item in tracks
    ]


def transfer_playlist(
    spotify_playlist_name: str,
    tidal_playlist_name: str,
    spotify_client: SpotifyClient,
    tidal_client: TidalClient,
    rewrite: bool = False,
):
    tracks: List[Dict] = spotify_client.load_playlist_tracks(spotify_playlist_name)
    parsed_tracks: List[Dict] = parse_spotify_tracks(tracks)

    tids = list()
    for track in tqdm(parsed_tracks, "Searching tracks on tidal..."):
        res: str | None = tidal_client.search_track(track)
        if not res:
            print(f"Skipped track {track['name']} {track['artist']}")
            continue
        tids.append(res)

    if not tids:
        print("No tracks found, playlist not created")
        return

    if rewrite:
        tidal_client.delete_playlist(tidal_playlist_name)

    playlist_desc = f"Created from spotify on {datetime.datetime.now()}"
    tidal_client.create_playlist(tidal_playlist_name, playlist_desc, tids)
