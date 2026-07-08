#!/bin/bash
# Auto-downloader: waits for quota replenishment then downloads sequentially
# Run: nohup bash auto_download.sh > download.log 2>&1 &

set -e
: "${COMTRADE_API_KEY_1:?Set COMTRADE_API_KEY_1 before running this archived downloader}"
SCRIPT="<repo-root>/04_scripts/download_comtrade.py"
LOG="<repo-root>/03_data/raw/download.log"

echo "$(date): Starting auto-downloader..." | tee -a "$LOG"

# Wait until quota is replenished (test every 5 min)
while true; do
STATUS=$(python3 -c "
import os
import requests
r = requests.get('https://comtradeapi.un.org/data/v1/get/C/M/HS', params={
    'reporterCode':'842','flowCode':'M','cmdCode':'811292','period':'202307',
    'subscription-key': os.environ['COMTRADE_API_KEY_1']
}, timeout=10)
print(r.status_code)
" 2>/dev/null || echo "error")
    
    if [ "$STATUS" = "200" ]; then
        echo "$(date): Quota replenished!" | tee -a "$LOG"
        break
    fi
    echo "$(date): Quota not ready (status=$STATUS), waiting 5 min..." | tee -a "$LOG"
    sleep 300
done

# Download treated HS codes one at a time
for HS in 811292 282560 2504 3801 8110 2617; do
    echo "$(date): Starting HS $HS imports..." | tee -a "$LOG"
    python3 "$SCRIPT" --mode imports --hs "$HS" 2>&1 | tee -a "$LOG"
    echo "$(date): Finished HS $HS" | tee -a "$LOG"
    sleep 10
done

# Download placebo HS codes one at a time
for HS in 2501 2523 2804 2818 2827 3815 3824 8111 8112; do
    echo "$(date): Starting placebo HS $HS imports..." | tee -a "$LOG"
    python3 "$SCRIPT" --mode imports --hs "$HS" 2>&1 | tee -a "$LOG"
    echo "$(date): Finished HS $HS" | tee -a "$LOG"
    sleep 10
done

echo "$(date): ALL DOWNLOADS COMPLETE" | tee -a "$LOG"

# Summary
echo "" | tee -a "$LOG"
echo "=== FILES ===" | tee -a "$LOG"
ls -la <repo-root>/03_data/raw/*.csv | tee -a "$LOG"
