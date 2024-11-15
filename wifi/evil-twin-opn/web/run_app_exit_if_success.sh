#!/bin/bash

python3 app.py "$@" &
app_pid=$!

file_check_interval=2

trap 'cleanup_and_exit' SIGINT

function cleanup_and_exit() {
    kill -SIGTERM $app_pid
    wait $app_pid 2>/dev/null

    pids=$(pgrep aireplay-ng)
    if [ -z "$pids" ]; then
        echo "Process 'aireplay-ng' not found."
    else
        for pid in $pids; do
            kill -SIGTERM "$pid"
            echo "Process $pid killed."
        done
    fi
    exit 0
}

while true; do
    if grep -q "OK" results.txt; then
        echo "Finded 'OK' in results.txt"

        exit
    else
        sleep $file_check_interval
    fi
done
