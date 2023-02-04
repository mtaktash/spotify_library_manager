import datetime
import json
import os
from typing import Dict, List

from tqdm import tqdm

from spotify_client import SpotifyClient
from tidal_client import TidalClient

LOGS_DIR = "logs"


def parse_spotify_track(track: Dict):
    return dict(
        name=track["track"]["name"],
        artist=track["track"]["artists"][0]["name"],
        album=track["track"]["album"]["name"],
        isrc=track["track"]["external_ids"]["isrc"],
    )


def transfer_playlist(
    spotify_playlist_name: str,
    tidal_playlist_name: str,
    spotify_client: SpotifyClient,
    tidal_client: TidalClient,
    rewrite: bool = False,
    save_missing_tracks: bool = False,
):
    timestamp = datetime.datetime.now()
        
    tracks: List[Dict] = spotify_client.load_playlist_tracks(spotify_playlist_name)
    missing_tracks = list()
    tids = list()
    for track in tqdm(tracks, "Searching tracks on tidal..."):
        parsed_track = parse_spotify_track(track)

        res: str | None = tidal_client.search_track(parsed_track)

        if not res:
            print(f"Skipped track {parsed_track['name']} {parsed_track['artist']}")
            if save_missing_tracks:
                missing_tracks.append(track)

            continue

        tids.append(res)

    if not tids:
        print("No tracks found, playlist not created")
        return

    if rewrite:
        tidal_client.delete_playlist(tidal_playlist_name)

    playlist_desc = f"Created from spotify on {timestamp}"
    tidal_client.create_playlist(tidal_playlist_name, playlist_desc, tids)

    if save_missing_tracks:
        os.makedirs(LOGS_DIR, exist_ok=True)
        filename = os.path.join(LOGS_DIR, f"missing_tracks_{timestamp}.json")
        
        print(f"Saving missing tracks to {filename}")
        parsed_missing_tracks = [parse_spotify_track(track) for track in missing_tracks]

        with open(filename, "w") as out:
            json.dump(parsed_missing_tracks, out)
