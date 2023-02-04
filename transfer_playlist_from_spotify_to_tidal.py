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
    parser.add_argument("spotify_playlist_name", help="Spotify playlist name or url")
    parser.add_argument(
        "tidal_playlist_name",
        help="Tidal playlist name, if empty, will create the playlist with --prefix ",
    )
    parser.add_argument(
        "-f",
        "--rewrite",
        action="store_true",
        help="If playlist with tidal_playlist_name exists, delete it and rewrite it",
    )
    parser.add_argument(
        "--prefix",
        help="Prefix to use with tidal playlist names, will use spotify user name if empty",
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

    transfer_playlist(
        args.spotify_playlist_name,
        args.tidal_playlist_name,
        args.prefix,
        spotify_client,
        tidal_client,
        args.rewrite,
    )
