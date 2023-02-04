set -e

if [[ $1 == "" ]]; then
    export PREFIX=""
else
    export PREFIX="$1"
fi 

# remove old file with playlist ids
export FILENAME="logs/temp_playlist_ids.txt"
rm -rf $FILENAME

# find playlist ids
python create_tidal_playlist_list.py $PREFIX

# download 
while IFS= read -r line; do
    echo $line 
    tidal-dl -l $line
done <<< $FILENAME

# clean up a bit
rm -rf $FILENAME
