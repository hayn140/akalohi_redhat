#!/bin/bash
# Place this file on Worker Node at /usr/local/bin/vmdk_webhoook_watcher.sh

# Configuration
WATCH_DIR="/var/lib/portkey/temp_data"
API_GATEWAY_URL="https://o7ahikdbf3.execute-api.us-east-2.amazonaws.com/dev/"
LOGFILE="/var/log/vmdk_webhook_watcher.log"
DELAY=5  # seconds to wait between file size checks

# Ensure log file exists and is writable
mkdir -p "$(dirname "$LOGFILE")"
touch "$LOGFILE"
chmod 644 "$LOGFILE"

log() {
  echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - $*" | tee -a "$LOGFILE"
}

# Declare function to wait until file size stops changing and is fully SCP'd over from RHSAT02
wait_for_complete() {
  local file="$1"
  local prev_size=-1
  local size=0

  log "Waiting for file $file to finish copying..."
  while true; do
    if [[ ! -f "$file" ]]; then
      log "File $file disappeared during wait, aborting."
      return 1
    fi

    size=$(stat -c%s "$file" 2>/dev/null)
    if [[ "$size" -eq "$prev_size" && "$size" -gt 0 ]]; then
      log "File $file size stable at $size bytes. Copy complete."
      return 0
    fi

    prev_size=$size
    sleep "$DELAY"
  done
}

# Declare function to invoke Lambda API Gateway URL for a given filename
invoke_lambda() {
  local file="$1"
  local payload
  payload=$(printf '{"filename":"%s"}' "$(basename "$file")")
  log "Invoking webhook for new VMDK: $file"

  resp=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$API_GATEWAY_URL" \
    -H "Content-Type: application/json" \
    -H "X-Webhook-Secret: $SECRET" \
    -d "$payload")

  body=$(echo "$resp" | sed -n '1,/HTTP_STATUS:/p' | sed '$d')
  status=$(echo "$resp" | tr -d '\r' | awk -F'HTTP_STATUS:' '{print $2}')

  log "Webhook response status: $status"
  log "Webhook response body: $body"
}

# Keep track of recent file events to avoid duplicates
declare -A seen_ts

# Main loop: Watch for create events
# -m: Monitor the directory forever
# -e create: Watch for a 'create' event, when a file is created or moved into this directory
# --format '%w%f': Return the output of the file with fullpath i.e. '/var/lib/portkey/temp_data/rhel9.6_noscap.vmdk'
# read -r filepath: Assign the fullpath of the found file to the filepath variable
inotifywait -m -e create --format '%w%f' "$WATCH_DIR" | while read -r filepath; do
  if [[ "$filepath" != *.vmdk ]]; then
    continue
  fi

  now=$(date +%s)
  last=${seen_ts["$filepath"]:-0}
  if (( now - last < DELAY )); then
    continue
  fi
  seen_ts["$filepath"]=$now

  if wait_for_complete "$filepath"; then # Calling function and waiting till file size stabilizes
    if [[ -s "$filepath" ]]; then
      invoke_lambda "$filepath" # Curling API Gateway URL
    else
      log "Skipping $filepath: file is empty after transfer." # Ensure the file is non-zero
    fi
  fi
done
