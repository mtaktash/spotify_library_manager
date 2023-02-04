import argparse
import os
from typing import List

from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm

from spotify_client import SpotifyClient
from tidal_client import TidalClient
from transfer_utils import transfer_playlist

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
    parser.add_argument(
        "-f",
        action="store_true",
        help="If playlist with tidal_playlist_name exists, delete it and rewrite it",
    )
    return parser.parse_args()


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
    if args.f:
        print(
            f'-f argument is given, rewriting playlist "{args.tidal_playlist_name}" on tidal'
        )

    transfer_playlist(
        args.spotify_playlist_name,
        args.tidal_playlist_name,
        spotify_client,
        tidal_client,
        args.f,
    )
