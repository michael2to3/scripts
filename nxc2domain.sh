#!/usr/bin/bash
awk '{ip=$2; match($0, /name:([^)]+)\) \(domain:([^)]+)\)/, arr); name=arr[1]; domain=arr[2]; print ip, name "." domain}'
