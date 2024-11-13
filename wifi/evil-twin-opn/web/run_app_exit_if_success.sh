#!/bin/bash

python3 app.py "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    pids=$(pgrep aireplay-ng)

    if [ -z "$pids" ]; then
        echo "Process aireplay-ng not found."
    else
        for pid in $pids; do
            kill -SIGTERM $pid
            echo "Send SIGTERM to $pid"
        done
    fi
else
    echo "Exit code: $exit_code"
fi
