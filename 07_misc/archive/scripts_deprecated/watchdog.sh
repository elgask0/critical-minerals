#!/bin/bash
# Watchdog: runs dl.py for one HS, kills after TIMEOUT, retries up to MAX times
# Usage: bash watchdog.sh HS_CODE

HS=$1
SCRIPT="<repo-root>/04_scripts/dl.py"
FINAL="<repo-root>/03_data/raw/comtrade_${HS}_imports.csv"
LOG="<repo-root>/03_data/raw/dl9_${HS}.log"
TIMEOUT=3600  # 60 minutes
MAX=20

if [ -f "$FINAL" ]; then
    echo "$(date): HS $HS already done"
    exit 0
fi

> "$LOG"

for i in $(seq 1 $MAX); do
    if [ -f "$FINAL" ]; then
        echo "$(date): HS $HS COMPLETE" | tee -a "$LOG"
        exit 0
    fi
    
    echo "$(date): HS $HS attempt $i/$MAX" | tee -a "$LOG"
    
    python3 -u "$SCRIPT" "$HS" >> "$LOG" 2>&1 &
    PID=$!
    
    elapsed=0
    while kill -0 $PID 2>/dev/null && [ $elapsed -lt $TIMEOUT ]; do
        sleep 10
        elapsed=$((elapsed + 10))
    done
    
    if kill -0 $PID 2>/dev/null; then
        echo "$(date): HS $hs timeout after ${TIMEOUT}s, killing" | tee -a "$LOG"
        kill $PID 2>/dev/null
        wait $PID 2>/dev/null
    else
        wait $PID 2>/dev/null
    fi
    
    if [ -f "$FINAL" ]; then
        echo "$(date): HS $HS COMPLETE on attempt $i" | tee -a "$LOG"
        exit 0
    fi
    
    echo "$(date): attempt $i failed, waiting 60s..." | tee -a "$LOG"
    sleep 60
done

echo "$(date): HS $HS FAILED after $MAX attempts" | tee -a "$LOG"
exit 1
