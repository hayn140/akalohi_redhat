#!/bin/bash
# Place this file on RHSAT02 at /usr/local/bin/vmdk_transfer.sh

# Configuration
WATCH_DIR="/var/lib/portkey/temp_data"
LOGFILE="/var/log/vmdk_transfer.log"
DELAY=2  # seconds to wait before acting on a new file (simple debounce)

# Ensure log file exists and is writable
mkdir -p "$(dirname "$LOGFILE")"
touch "$LOGFILE"
chmod 644 "$LOGFILE"

# Declare Log Function
log() {
  echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - $*" | tee -a "$LOGFILE"
}

# Declare SCP Copy Function
transfer_to_worker_node() {
  FOUND_FILE="$1"
  SSH_USER="rh-ansible"
  PRIVATE_KEY_FILE="/home/rh-ansible/.ssh/rh-ansible"
  SOURCE_SERVER="ncmd-ff-rhsat02.ncmd.nsa.ic.gov"
  DEST_SERVER="nctx-ff-aapw02.nctx.nsa.ic.gov"
  DEST_DIR="$WATCH_DIR"
  
  log "Starting SCP transfer: $(basename "$FOUND_FILE") -> $DEST_SERVER:$DEST_DIR"

  # Initiate Transfer to Worker Node
  if scp -i "$PRIVATE_KEY_FILE" "$FOUND_FILE" "$SSH_USER@$DEST_SERVER:$DEST_DIR/"; then
    log "Transfer complete: $(basename "$FOUND_FILE")"
    rm -f "$FOUND_FILE" && log "Deleted local file: $(basename "$FOUND_FILE")"
  else
    log "ERROR: Transfer failed for $(basename "$FOUND_FILE")"
  fi

  # Remove file once it's done being transferred to the worker-node
  rm -rf $FOUND_FILE
}

# Keep track of recent file events to avoid duplicates
declare -A seen_ts

# Main loop: Watch for create/moved_to events
# -m: Monitor the directory forever
# -e create: Watch for a 'create' event, when a file is created
# -e moved_to: Watch for a 'moved' event, when a file is moved into the directory
# --format '%w%f': Return the output of the file with fullpath
# read -r filepath: Assign the fullpath of the found file to the filepath variable
inotifywait -m -e create -e moved_to --format '%w%f' "$WATCH_DIR" | while read -r FILEPATH; do

  # Only act on .vmdk files
  if [[ "$FILEPATH" != *.vmdk ]]; then
    continue
  fi

  # Simple debounce: if seen this file very recently, skip
  now=$(date +%s)
  last=${seen_ts["$FILEPATH"]:-0}
  if (( now - last < DELAY )); then
    continue
  fi
  seen_ts["$FILEPATH"]=$now

  # Optional: wait a moment to ensure file is fully written
  sleep $DELAY

  # Double-check file still exists and is non-zero
  if [[ -s "$FILEPATH" ]]; then
  # Copy the file over to the worker-node
    transfer_to_worker_node "$FILEPATH"
  else
    log "Skipping $FILEPATH: file missing or empty after wait"
  fi
done
