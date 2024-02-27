#!/bin/bash

set -e

KEY_DIR=~/Keys
FILE_TO_ENCRYPT=$1
FILE_OUT="$1.gpg"
NO_HOOK=$2
HOOK='ripdrag'

GPG_CMD="gpg --trust-model=always"

for key in "$KEY_DIR"/*.*; do
    gpg --import "$key"

    KEY_ID=$(gpg --with-colons --list-keys | grep '^pub' | awk -F: '{print $5}' | grep -F -x -f <(gpg --with-colons --import-options show-only --import "$key" | grep '^pub' | awk -F: '{print $5}'))
    if [[ -z "$KEY_ID" ]]; then
      echo "Key not found in $key"
      gpg --import "$key"
      KEY_ID=$(gpg --with-colons --import-options show-only --import "$key" | grep '^pub' | awk -F: '{print $5}')
    fi
    GPG_CMD="$GPG_CMD -r $KEY_ID"
done

GPG_CMD="$GPG_CMD  -o $FILE_OUT -e $FILE_TO_ENCRYPT"

echo "Running command: $GPG_CMD"
eval "$GPG_CMD"

if [ -z "$NO_HOOK" ]; then
 eval $HOOK "$FILE_OUT"
fi
