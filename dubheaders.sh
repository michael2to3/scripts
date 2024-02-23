#!/usr/bin/bash

url="$1"

if [ -z "$url" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

headers=$(curl --connect-timeout 2 -s -D - "$url" -o /dev/null | tr -d '\r')

echo "$headers" | awk 'NF {
    count[$1]++
}
END {
    for (header in count)
        if (count[header] > 1)
            print header
}' | sed 's/://'
