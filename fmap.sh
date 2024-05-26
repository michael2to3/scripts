#!/bin/bash

fmap() {
  local args=("$@")
  local scan_type=""
  local ip_version=""
  local targets=""
  for arg in "${args[@]}"; do
    if [[ "$arg" != -* ]]; then
      targets=$arg
    fi
    case "$arg" in
      -sT|-sS|-sA|-sW|-sM)
        scan_type=$arg
        ;;
      -6)
        ip_version="-6"
        ;;
    esac
  done
  p=$(nmap -T5 --min-rate=1000 -p- $scan_type $ip_version "$targets" --open | grep '^[0-9]' | cut -d '/' -f1 | tr '\n' ',' | sed 's/,$//')
  nmap -p$p "${args[@]}"
}
