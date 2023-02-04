set -e

export FILENAME=$1
export SAVE_MISSING_PATH="logs/playlist_list_missing_$(date +"%Y-%m-%d-%T").json"

while IFS= read -r line; do
    python transfer_playlist_from_spotify_to_tidal.py -f --save_missing --save_missing_path "$SAVE_MISSING_PATH" "$line" ""
done < $FILENAME
