import argparse
import os
from typing import List

from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm

from spotify_client import SpotifyClient
from tidal_client import TidalClient

load_dotenv(find_dotenv())

SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPE: str = os.getenv("SPOTIFY_SCOPE")

TIDAL_TOKEN_TYPE: str = os.getenv("TIDAL_TOKEN_TYPE")
TIDAL_ACCESS_TOKEN: str = os.getenv("TIDAL_ACCESS_TOKEN")
TIDAL_REFRESH_TOKEN: str = os.getenv("TIDAL_REFRESH_TOKEN")
TIDAL_EXPIRY_TIME: str = os.getenv("TIDAL_EXPIRY_TIME")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("spotify_playlist_name")
    parser.add_argument("tidal_playlist_name")
    return parser.parse_args()


def parse_spotify_tracks(tracks: List):
    return [
        dict(
            name=item["track"]["name"],
            artist=item["track"]["artists"][0]["name"],
            isrc=item["track"]["external_ids"]["isrc"],
        )
        for item in tracks
    ]


def transfer_playlist(
    spotify_playlist_name: str,
    tidal_playlist_name: str,
    spotify_client: SpotifyClient,
    tidal_client: TidalClient,
):
    tracks = spotify_client.load_playlist_tracks(spotify_playlist_name)
    parsed_tracks = parse_spotify_tracks(tracks)
    tids = list()
    for track in tqdm(parsed_tracks, "Searching tracks on tidal..."):
        res: str | None = tidal_client.search_track(track)
        if not res:
            print(f"Skipped track {track['name']} {track['artist']}")
            continue
        tids.append(res)
    tidal_client.add_to_playlist(tidal_playlist_name, tids)


if __name__ == "__main__":
    args = parse_args()
    spotify_client = SpotifyClient(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
    )

    tidal_client = TidalClient(
        token_type=TIDAL_TOKEN_TYPE,
        access_token=TIDAL_ACCESS_TOKEN,
        refresh_token=TIDAL_REFRESH_TOKEN,
        expiry_time=TIDAL_EXPIRY_TIME,
    )

    print("Connecting to Spotify account...")
    spotify_client.login()

    print("Connecting to Tidal account...")
    tidal_client.login()

    print(
        f'Transferring spotify playlist "{args.spotify_playlist_name}" to tidal playlist "{args.tidal_playlist_name}"'
    )
    transfer_playlist(
        args.spotify_playlist_name,
        args.tidal_playlist_name,
        spotify_client,
        tidal_client,
    )
