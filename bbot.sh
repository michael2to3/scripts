#!/bin/bash

add_volume_if_exists() {
    local DIR_NAME="$1"
    local MOUNT_POINT="$2"
    local DOCKER_VOLUMES_VAR="$3"

    if [ -d "$DIR_NAME" ]; then
        local ABS_DIR_PATH
        ABS_DIR_PATH=$(realpath "$DIR_NAME")
        eval "$DOCKER_VOLUMES_VAR+=(-v \"$ABS_DIR_PATH:$MOUNT_POINT\")"
    fi
}

OUTPUT_DIR=""
ARGS=("$@")
for ((i = 0; i < $#; i++)); do
    if [ "${ARGS[$i]}" == "-o" ]; then
        OUTPUT_DIR="${ARGS[$i+1]}"
        break
    fi
done

if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="./output"
fi

ABS_OUTPUT_DIR=$(realpath "$OUTPUT_DIR")

NEW_ARGS=()
SKIP_NEXT=false
for arg in "${ARGS[@]}"; do
    if [ "$SKIP_NEXT" = true ]; then
        SKIP_NEXT=false
        continue
    fi
    if [ "$arg" == "-o" ]; then
        SKIP_NEXT=true
        continue
    fi
    NEW_ARGS+=("$arg")
done

DOCKER_VOLUMES=()
DOCKER_VOLUMES+=("-v \"$ABS_OUTPUT_DIR:/root/output\"")
DOCKER_VOLUMES+=("-v \"$HOME/.bbot:/root/.bbot\"")
DOCKER_VOLUMES+=("-v \"$HOME/.config/bbot:/root/.config/bbot\"")

add_volume_if_exists "$HOME/Wordlists" "/root/Wordlists" DOCKER_VOLUMES
add_volume_if_exists "$HOME/cent-nuclei-templates/" "/root/cent-nuclei-template" DOCKER_VOLUMES
add_volume_if_exists "$HOME/nuclei-templates/" "/root/nuclei-template" DOCKER_VOLUMES

eval "docker run --network host --rm -it ${DOCKER_VOLUMES[@]} dockeronfullpc/fat-bbot:dev -o /root/output \"${NEW_ARGS[@]}\""
