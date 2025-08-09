#!/bin/bash

# Configuration
WATCH_DIR="/var/lib/portkey/temp_data"
LOGFILE="/var/log/vmdk_transfer.log"
DELAY=2  # seconds to wait before acting on a new file (simple debounce)

# Ensure log file exists and is writable
mkdir -p "$(dirname "$LOGFILE")"
touch "$LOGFILE"
chmod 644 "$LOGFILE"

log() {
  echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - $*" | tee -a "$LOGFILE"
}

transfer_to_worker_node() {
  FOUND_FILE="$1"
  PRIVATE_KEY_FILE="/home/ec2-user/.ssh/akalohi-aws.pem"
  SSH_USER="rh-ansible"
  SOURCE_SERVER="ncmd-ff-rhsat02.ncmd.nsa.ic.gov"
  SOURCE_DIR="$WATCH_DIR"
  DEST_SERVER="nctx-ff-aapw02.nctx.nsa.ic.gov"
  DEST_DIR="$WATCH_DIR"

  scp -i $PRIVATE_KEY_FILE $SOURCE_DIR/$FOUND_FILE $SSH_USER@$DEST_SERVER:$DEST_DIR/
}

# Keep track of recent file events to avoid duplicates
declare -A seen_ts

# Main loop: Watch for create/moved_to events
inotifywait -m -e create -e moved_to --format '%w%f' "$WATCH_DIR" | while read -r filepath; do
  # Only act on .vmdk files
  if [[ "$filepath" != *.vmdk ]]; then
    continue
  fi

  # Simple debounce: if seen this file very recently, skip
  now=$(date +%s)
  last=${seen_ts["$filepath"]:-0}
  if (( now - last < DELAY )); then
    continue
  fi
  seen_ts["$filepath"]=$now

  # Optional: wait a moment to ensure file is fully written
  sleep $DELAY

  # Double-check file still exists and is non-zero
  if [[ -s "$filepath" ]]; then
    transfer_to_worker_node "$filepath"
  else
    log "Skipping $filepath: file missing or empty after wait"
  fi
done
