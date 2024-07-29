#!/bin/bash

VOLUME=""
CONTAINER_NAME="mkali"

if [ $# -gt 0 ]; then
    for ARG in "$@"
    do
        VOLUME="$VOLUME -v $ARG:/root/$(basename $ARG)"
    done
fi

#apt update && apt -y install kali-linux-headless
#apt update && apt -y install kali-linux-large
docker run \
    --name "$CONTAINER_NAME" \
    --mount src=kali-root,dst=/root \
    --mount src=kali-postgres,dst=/var/lib/postgresql \
    -ti \
    $VOLUME \
    kalilinux/kali-rolling:latest

docker commit "$CONTAINER_NAME" kalilinux/kali-rolling:latest

docker rm "$CONTAINER_NAME"
