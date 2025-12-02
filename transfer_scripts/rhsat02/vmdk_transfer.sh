#!/bin/bash
# Place this file on RHSAT02 at /usr/local/bin/vmdk_transfer.sh

# Configuration
WATCH_DIR=""
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

# Declare function to wait until file size stops changing and is fully Uploaded from EVO S3

wait_for_complete() {
  local file="$1"
  local prev_size=-1
  local size=0

  log "Waiting for file $file to finish uploading from EVO..."
  while true; do
    if [[ ! -f "$file" ]]; then
      log "File $file disappeared during wait, aborting."
      return 1
    fi

    size=$(stat -c%s "$file" 2>/dev/null)
    if [[ "$size" -eq "$prev_size" && "$size" -gt 0 ]]; then
      log "File $file size stable at $size bytes. Upload from EVO complete."
      return 0
    fi

    prev_size=$size
    sleep "$DELAY"
  done
}


# Declare SCP Copy Function
transfer_to_worker_node() {
  FOUND_FILE="$1"
  SSH_USER="rh-ansible"
  PRIVATE_KEY_FILE=""
  DEST_SERVER=""
  DEST_DIR="/home/$SSH_USER/transferred_vmdk_files"
  
  log "Starting SCP transfer: $(basename "$FOUND_FILE") -> $DEST_SERVER:$DEST_DIR"

  # Initiate Transfer to Worker Node
  if scp -i "$PRIVATE_KEY_FILE" "$FOUND_FILE" "$SSH_USER@$DEST_SERVER:$DEST_DIR"; then
    log "Transfer complete: $(basename "$FOUND_FILE")"
    # Remove file once it's done being transferred to the worker-node
    rm -f "$FOUND_FILE" && log "Deleted local file: $(basename "$FOUND_FILE")"
  else
    log "ERROR: Transfer failed for $(basename "$FOUND_FILE")"
  fi
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
  # Extract filename from full path
  FILENAME=$(basename $FILEPATH)
  # Only act on .vmdk files
  if [[ "$FILEPATH" != *noscap*.vmdk || "$FILENAME" == .* ]]; then
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

  if wait_for_complete "$FILEPATH"; then # Calling function and waiting till file size stabilizes
    # Double-check file still exists and is non-zero
    if [[ -s "$FILEPATH" ]]; then
    # Copy the file over to the worker-node
      transfer_to_worker_node "$FILEPATH" # Calling SCP function to transfer file over to Worker Node
    else
      log "Skipping $FILEPATH: file missing or empty after wait"
    fi
  fi
done

