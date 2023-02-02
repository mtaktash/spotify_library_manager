import argparse
from typing import List

from tqdm import tqdm

from spotify_client import SpotifyClient
from tidal_client import TidalClient


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("spotify_playlist_name")
    parser.add_argument("tidal_playlist_name")
    parser.add_argument("--client_id")
    parser.add_argument("--client_secret")
    parser.add_argument("--redirect_uri", default="http://127.0.0.1:9090")
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


if __name__ == "__main__":
    args = parse_args()
    spotify_client = SpotifyClient(
        client_id=args.client_id,
        client_secret=args.client_secret,
        redirect_uri=args.redirect_uri,
        scope="user-library-read",
    )

    tidal_client = TidalClient()

    print("Connecting to Spotify account...")
    spotify_client.login()

    print("Connecting to Tidal account...")
    tidal_client.login()

    print("Loading Spotify playlist tracks...")
    tracks = spotify_client.load_playlist_tracks(args.spotify_playlist_name)
    parsed_tracks = parse_spotify_tracks(tracks)

    print("Searching Tidal...")
    tids = list()
    for track in tqdm(parsed_tracks):
        res: str | None = tidal_client.search_track(track)
        if not res:
            print(f"Skipped track {track['name']} {track['artist']}")
            continue
        tids.append(res)

    tidal_client.add_to_playlist(args.tidal_playlist_name, tids)
