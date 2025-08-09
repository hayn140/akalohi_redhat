#!/bin/bash
# Place this file on Worker Node at /usr/local/bin/vmdk_webhook_watcher.sh

# Configuration
WATCH_DIR="/var/lib/portkey/temp_data"
FUNCTION_URL="https://3stdeqd4prm7wp24vbsxxc34ne0zcfia.lambda-url.us-east-2.on.aws/"
SECRET="s3cr3t-token-123"   # or export WEBHOOK_SECRET in environment and use ${WEBHOOK_SECRET}
LOGFILE="/var/log/vmdk_webhook_watcher.log"
DELAY=2  # seconds to wait before acting on a new file (simple debounce)

# Ensure log file exists and is writable
mkdir -p "$(dirname "$LOGFILE")"
touch "$LOGFILE"
chmod 644 "$LOGFILE"

log() {
  echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - $*" | tee -a "$LOGFILE"
}

# Function to invoke Lambda for a given file path
invoke_lambda() {
  local file="$1"
  local payload
  payload=$(printf '{"filename":"%s"}' "$(basename "$file")")
  log "Invoking webhook for new VMDK: $file"

  # Perform the curl and capture status/body
  resp=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$FUNCTION_URL" \
    -H "Content-Type: application/json" \
    -H "X-Webhook-Secret: $SECRET" \
    -d "$payload")
  body=$(echo "$resp" | sed -n '1,/HTTP_STATUS:/p' | sed '$d')
  status=$(echo "$resp" | tr -d '\r' | awk -F'HTTP_STATUS:' '{print $2}')

  log "Webhook response status: $status"
  log "Webhook response body: $body"

  if [[ "$status" == "200" ]]; then
    log "Successfully triggered lambda for $file"
  else
    log "Failed to trigger lambda for $file"
  fi
}

# Keep track of recent file events to avoid duplicates
declare -A seen_ts

# Main loop: watch for create/moved_to events
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
    invoke_lambda "$filepath"
  else
    log "Skipping $filepath: file missing or empty after wait"
  fi
done
