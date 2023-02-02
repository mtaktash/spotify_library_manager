import argparse
from pprint import pprint
from spotify_manager import SpotifyClient


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client_id")
    parser.add_argument("--client_secret")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    spotify_client = SpotifyClient(
        client_id=args.client_id,
        client_secret=args.client_secret,
        redirect_uri="http://127.0.0.1:9090",
        scope="user-library-read",
    )

    spotify_client.login()

    pprint(spotify_client.sp.me())