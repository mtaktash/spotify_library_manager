import datetime
import json
import os
from typing import Dict, List

from tqdm import tqdm

from spotify_client import SpotifyClient
from tidal_client import TidalClient


def parse_spotify_track(track: Dict):
    return dict(
        name=track["track"]["name"],
        artist=track["track"]["artists"][0]["name"],
        album=track["track"]["album"]["name"],
        isrc=track["track"]["external_ids"]["isrc"],
        spotify_id=track["track"]["id"],
    )


def transfer_playlist(
    spotify_playlist_name: str,
    tidal_playlist_name: str,
    prefix: str,
    spotify_client: SpotifyClient,
    tidal_client: TidalClient,
    rewrite: bool = False,
    save_missing: bool = False,
    save_missing_path: str = None,
):
    spotify_playlist = spotify_client.load_playlist(spotify_playlist_name)
    tracks: List[Dict] = spotify_client.load_playlist_tracks(spotify_playlist)

    if not prefix:
        prefix = spotify_client.get_user_name()

    tidal_playlist_name = f"{prefix} {spotify_playlist['name']}"
    print(
        f'\nTransferring spotify playlist "{spotify_playlist["name"]}" to tidal playlist "{tidal_playlist_name}"'
    )
    if rewrite:
        print(
            f'--rewrite argument is given, rewriting playlist "{tidal_playlist_name}" on tidal'
        )

    missing_tracks = list()
    tids = list()
    for track in tqdm(tracks, "Searching tracks on tidal..."):
        parsed_track = parse_spotify_track(track)

        res: str | None = tidal_client.search_track(parsed_track)

        if not res:
            print(f"Skipped track {parsed_track['name']} {parsed_track['artist']}")
            if save_missing:
                missing_tracks.append(track)
            continue

        tids.append(res)

    if not tids:
        print("No tracks found, playlist not created")
        return

    if rewrite:
        tidal_client.delete_playlist(tidal_playlist_name)

    playlist_desc = f"Created from spotify playlist {spotify_playlist['external_urls']['spotify']} on {datetime.datetime.now()}"
    tidal_client.create_playlist(tidal_playlist_name, playlist_desc, tids)

    if save_missing:
        print(f"Saving missing tracks to {save_missing_path}")
        parsed_missing_tracks = [parse_spotify_track(track) for track in missing_tracks]
        all_missing_tracks = list()

        if os.path.exists(save_missing_path):
            with open(save_missing_path, "r", encoding="utf-8") as f:
                loaded_missing_tracks = json.load(f)
            all_missing_tracks.extend(loaded_missing_tracks)

        all_missing_tracks.extend(parsed_missing_tracks)

        with open(save_missing_path, "w", encoding="utf-8") as f:
            json.dump(all_missing_tracks, f)
