#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/scripts/demo_start.sh"
STATUS=$?
echo
if [ "$STATUS" -eq 0 ]; then
  echo "Demo startup finished. Open http://localhost:8000"
else
  echo "Demo startup failed. Please copy the messages above."
fi
echo "Press Enter to close this window."
read -r
exit "$STATUS"
