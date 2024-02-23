#!/usr/bin/python3

import argparse
import logging
import requests
import urllib3
from collections import defaultdict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domains", nargs="+")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("--check-ssl", action="store_true", help="Enable SSL verification")
args = parser.parse_args()

logging_level = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(level=logging_level)

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


def check_headers(domain):
    headers_to_check = [
        "X-Content-Type-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
    ]
    headers = {"User-Agent": user_agent}
    missing_headers = []
    try:
        response = requests.get(
            f"https://{domain}", headers=headers, timeout=5, verify=args.check_ssl
        )
        for header in headers_to_check:
            if header not in response.headers:
                missing_headers.append(header)
    except requests.RequestException as e:
        logging.error(f"Error fetching {domain}: {e}")
    return missing_headers


def group_by_missing_headers(domains):
    missing_headers_group = defaultdict(list)
    for domain in domains:
        missing_headers = check_headers(domain)
        key = ", ".join(sorted(missing_headers))
        missing_headers_group[key].append(domain)
    return missing_headers_group


def print_grouped_results(missing_headers_group):
    for missing_headers, domains in missing_headers_group.items():
        if missing_headers:  # Only print if there are missing headers
            print(f"{', '.join(domains)}:")
            for header in missing_headers.split(", "):
                print(f"- {header}")


if __name__ == "__main__":
    if not args.domains:
        logging.error("No domains provided. Use -d to specify domains.")
    else:
        missing_headers_group = group_by_missing_headers(args.domains)
        print_grouped_results(missing_headers_group)
