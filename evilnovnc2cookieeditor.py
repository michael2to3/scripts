#!/usr/bin/env python3

import argparse
import datetime
import json
import sys
from typing import Any, Dict, List


def parse_input(data: str) -> List[Dict[str, Any]]:
    if not data.strip():
        sys.exit("No input data provided.")

    separator = "=" * 62
    blocks = data.strip().split(separator)
    cookies = []

    for block in blocks:
        lines = block.strip().split("\n")
        if not lines:
            continue

        cookie: Dict[str, Any] = {}
        for line in lines:
            if not line.strip():
                continue
            if ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip()
                value = value.strip()
                if key == "Host":
                    cookie["domain"] = value
                elif key == "Cookie name":
                    cookie["name"] = value
                elif key == "Cookie value (decrypted)":
                    cookie["value"] = value
                elif key == "Expires datetime (UTC)":
                    if value:
                        try:
                            dt = datetime.datetime.strptime(
                                value, "%Y-%m-%d %H:%M:%S.%f"
                            )
                        except ValueError:
                            try:
                                dt = datetime.datetime.strptime(
                                    value, "%Y-%m-%d %H:%M:%S"
                                )
                            except ValueError:
                                dt = None
                        if dt:
                            cookie["expirationDate"] = dt.timestamp()
                    else:
                        cookie["session"] = True
            else:
                continue

        domain = cookie.get("domain", "")
        cookie["hostOnly"] = not domain.startswith(".")
        cookie["path"] = "/"
        cookie["secure"] = False
        cookie["httpOnly"] = False
        cookie["sameSite"] = None
        cookie["storeId"] = None
        cookie["session"] = cookie.get("session", False)

        if "expirationDate" not in cookie:
            cookie["session"] = True

        cookies.append(cookie)

    return cookies


def main():
    parser = argparse.ArgumentParser(description="Convert cookie data to JSON format.")
    parser.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r", encoding="utf-8"),
        default=sys.stdin,
        help="Input file (default: stdin)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w", encoding="utf-8"),
        default=sys.stdout,
        help="Output file (default: stdout)",
    )
    args = parser.parse_args()

    input_data = args.input.read()
    if not input_data.strip():
        sys.exit("No input data provided.")

    cookies = parse_input(input_data)

    json.dump(cookies, args.output, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
