#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/scripts/demo_stop.sh"
STATUS=$?
echo
if [ "$STATUS" -eq 0 ]; then
  echo "Demo stopped."
else
  echo "Stopping failed. Please copy the messages above."
fi
echo "Press Enter to close this window."
read -r
exit "$STATUS"

