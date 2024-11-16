#!/bin/bash

OUTPUT_DIR="/media/data"

if ! command -v adb &>/dev/null; then
    echo "adb not found"
    exit 1
fi

if ! command -v ffmpeg &>/dev/null; then
    echo "ffmpeg not found"
    exit 1
fi

TIMESTAMP=$(date +'%d.%m.%y_%H%M')
DEVICE=$(adb shell getprop ro.product.model | tr -d ' \r\n')
OUTPUT_FILE="$OUTPUT_DIR/${TIMESTAMP}_${DEVICE}.mp4"
DEVICE_COUNT=$(adb devices | grep -w "device" | wc -l)
if [ "$DEVICE_COUNT" -eq "0" ]; then
    echo "device not found"
    exit 1
fi

echo "start record from $DEVICE..."
adb exec-out screenrecord --output-format=h264 - | ffmpeg -y -f h264 -i - -vf scale=480:-2 -vcodec libx264 -preset veryfast -crf 28 "$OUTPUT_FILE"
echo "save in $OUTPUT_FILE."
