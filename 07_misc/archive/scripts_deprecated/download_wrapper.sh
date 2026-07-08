#!/bin/bash
# Resilient download wrapper: restarts the Python script if it dies
# Usage: bash download_wrapper.sh

set -e
SCRIPT="<repo-root>/04_scripts/download_comtrade.py"
LOGDIR="<repo-root>/03_data/raw"

# Treated HS codes (811292 already done)
TREATED="282560 2504 3801 8110 2617"
# Placebo HS codes
PLACEBO="2501 2523 2804 2818 2827 3815 3824 8111 8112"

for HS in $TREATED $PLACEBO; do
    echo "$(date): === Starting HS $HS ==="
    
    FINAL="<repo-root>/03_data/raw/comtrade_${HS}_imports.csv"
    if [ -f "$FINAL" ]; then
        echo "$(date): HS $HS already done, skipping"
        continue
    fi
    
    MAX_RETRIES=10
    RETRY=0
    while [ ! -f "$FINAL" ] && [ $RETRY -lt $MAX_RETRIES ]; do
        RETRY=$((RETRY + 1))
        echo "$(date): HS $HS attempt $RETRY/$MAX_RETRIES"
        
        python3 -u "$SCRIPT" --mode imports --hs "$HS" >> "$LOGDIR/dl_${HS}.log" 2>&1 &
        PY_PID=$!
        
        # Wait up to 3600s (1 hour)
        WAITED=0
        while kill -0 $PY_PID 2>/dev/null && [ $WAITED -lt 3600 ]; do
            sleep 10
            WAITED=$((WAITED + 10))
        done
        
        # If still running after 1 hour, kill it
        if kill -0 $PY_PID 2>/dev/null; then
            kill $PY_PID 2>/dev/null
        fi
        
        # Wait for process to finish
        wait $PY_PID 2>/dev/null || true
        
        if [ -f "$FINAL" ]; then
            echo "$(date): HS $HS COMPLETE"
            break
        fi
        
        echo "$(date): HS $HS attempt $RETRY failed, waiting 30s..."
        sleep 30
    done
    
    if [ ! -f "$FINAL" ]; then
        echo "$(date): HS $HS FAILED after $MAX_RETRIES attempts"
    fi
    
    sleep 5
done

echo "$(date): ALL DONE"
ls -la <repo-root>/03_data/raw/comtrade_*_imports.csv
