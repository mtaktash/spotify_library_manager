import argparse
import os

from dotenv import load_dotenv, find_dotenv

from tidal_client import TidalClient

load_dotenv(find_dotenv())

TIDAL_TOKEN_TYPE: str = os.getenv("TIDAL_TOKEN_TYPE")
TIDAL_ACCESS_TOKEN: str = os.getenv("TIDAL_ACCESS_TOKEN")
TIDAL_REFRESH_TOKEN: str = os.getenv("TIDAL_REFRESH_TOKEN")
TIDAL_EXPIRY_TIME: str = os.getenv("TIDAL_EXPIRY_TIME")

ID_FILENAME: str = "logs/temp_playlist_ids.txt"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prefix",
        required=False,
        help="Prefix to use with tidal playlist names, will use spotify user name if empty",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    tidal_client = TidalClient(
        token_type=TIDAL_TOKEN_TYPE,
        access_token=TIDAL_ACCESS_TOKEN,
        refresh_token=TIDAL_REFRESH_TOKEN,
        expiry_time=TIDAL_EXPIRY_TIME,
    )

    print("Connecting to Tidal account...")
    tidal_client.login()

    all_playlists = tidal_client.load_all_user_playlists()
    all_ids = []
    for playlist in all_playlists:
        if not args.prefix or (args.prefix and playlist.name.startswith(args.prefix)):
            all_ids.append(playlist.id)

    print(f"Writing ids to {ID_FILENAME}")
    with open(ID_FILENAME, "w") as f:
        f.write("\n".join(all_ids))
