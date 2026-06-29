#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/scripts/demo_reset.sh"
STATUS=$?
echo
if [ "$STATUS" -eq 0 ]; then
  echo "Demo reset finished. Open http://localhost:8000"
else
  echo "Demo reset failed. Please copy the messages above."
fi
echo "Press Enter to close this window."
read -r
exit "$STATUS"
