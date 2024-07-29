#!/usr/bin/bash

ipv4_regex='\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

if [ -n "$1" ]; then
    input_file="$1"
    grep -oP "$ipv4_regex" "$input_file"
else
    grep -oP "$ipv4_regex"
fi
