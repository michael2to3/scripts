#!/usr/bin/env bash

pids=()

cleanup() {
    echo cleanup
    for pid in "${pids[*]}"
    do
        kill $pid
    done
}
trap cleanup 0
trap cleanup SIGKILL

for arg in "$@"
do
    swgui "$arg" &
    pids+=("$!")
done

read && exit
cleanup
