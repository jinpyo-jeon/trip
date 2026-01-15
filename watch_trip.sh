#!/bin/bash
# File watcher for trip.md - polls every 2 seconds

WATCH_FILE="/home/jin/trip.md"
LAST_HASH=""

get_hash() {
    md5sum "$WATCH_FILE" 2>/dev/null | cut -d' ' -f1
}

LAST_HASH=$(get_hash)
echo "Watching $WATCH_FILE for changes..."
echo "Initial hash: $LAST_HASH"

while true; do
    sleep 2
    CURRENT_HASH=$(get_hash)

    if [ "$CURRENT_HASH" != "$LAST_HASH" ] && [ -n "$CURRENT_HASH" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - CHANGE DETECTED in trip.md"
        echo "Old hash: $LAST_HASH"
        echo "New hash: $CURRENT_HASH"
        LAST_HASH=$CURRENT_HASH
    fi
done
