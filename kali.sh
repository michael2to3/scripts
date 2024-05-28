#!/bin/bash

VOLUME=""

if [ $# -gt 0 ]; then
    for ARG in "$@"
    do
        VOLUME="$VOLUME -v $ARG:/root/$(basename $ARG)"
    done
fi

#apt update && apt -y install kali-linux-headless
#apt update && apt -y install kali-linux-large
docker run \
    --mount src=kali-root,dst=/root \
    --mount src=kali-postgres,dst=/var/lib/postgresql \
    -ti \
    $VOLUME \
    kalilinux/kali-rolling
