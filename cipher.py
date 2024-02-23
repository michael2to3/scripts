import time
import logging
import argparse
from pathlib import Path
from typing import Dict, Set, Tuple, List
import requests
from hashlib import sha256
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--no-cache", action="store_true", help="Disable cache")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
args = parser.parse_args()

logging_level = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(level=logging_level)

CACHE_FILE = Path.home() / ".ciphersuite_cache.html"
CACHE_EXPIRY = 7 * 24 * 60 * 60


def fetch_data() -> str:
    use_cache = not args.no_cache
    if (
        use_cache
        and CACHE_FILE.exists()
        and (time.time() - CACHE_FILE.stat().st_mtime < CACHE_EXPIRY)
    ):
        logging.info("Using cached version of ciphersuite.info")
        return CACHE_FILE.read_text(encoding="utf-8")
    logging.info("Fetching new version of ciphersuite.info")
    response = requests.get("https://ciphersuite.info/cs/?singlepage=true")
    CACHE_FILE.write_text(response.text, encoding="utf-8")
    return response.text


def parse_xml(xml_data: str) -> Dict[str, Dict[str, Set[str]]]:
    try:
        root = ET.fromstring(xml_data)
        return process_hosts(root)
    except ET.ParseError:
        print("Error parsing XML data. Please ensure the input is valid XML.")
        return {}


def process_hosts(root: ET.Element) -> Dict[str, Dict[str, Set[str]]]:
    return {
        (
            host.find(".//hostname").get("name")
            if host.find(".//hostname") is not None
            else host.find(".//address").get("addr")
        ): {
            table.get("key"): {
                elem.text for elem in table.findall(".//elem[@key='name']")
            }
            for script in host.findall(".//script[@id='ssl-enum-ciphers']")
            for table in script.findall(".//table")
            if table.get("key") and table.findall(".//table[@key='ciphers']")
        }
        for host in root.findall(".//host")
    }


def grouped_by_domain(
    data: Dict[str, Dict[str, Set[str]]]
) -> Tuple[Dict[str, Dict[str, Set[str]]], Dict[str, List[str]]]:
    cipher = {}
    grouped_data = {}
    for domain, tls in data.items():
        for tls_version, ciphers in tls.items():
            key = sha256("|".join(sorted([tls_version, *ciphers])).encode()).hexdigest()
            cipher[key] = {"version": tls_version, "ciphers": ciphers}
            grouped_data.setdefault(key, []).append(domain)
    return cipher, grouped_data


def print_grouped_items(
    cipher: Dict[str, Dict[str, Set[str]]],
    data: Dict[str, List[str]],
    db: Dict[str, str],
):
    for key, domains in sorted(data.items()):
        ciphers = sorted([
            c
            for c in cipher[key]["ciphers"]
            if c in db and db[c] not in ["Recommended", "Secure"]
        ])
        if ciphers:
            print("   Domains: ", ", ".join(domains), sep=" ")
            print(f"   Version: {cipher[key]['version']}")
            print(*ciphers, sep="\n")
            print()


if __name__ == "__main__":
    html_content = fetch_data()
    soup = BeautifulSoup(html_content, "html.parser")
    db = {
        cipher.text: badge.text
        for el in soup.select("li")
        if (badge := el.select_one(".badge"))
        and (cipher := el.select_one(".break-all"))
    }

    xml_data = sys.stdin.read()
    domain_tls_map = parse_xml(xml_data)

    cipher, grouped_data = grouped_by_domain(domain_tls_map)
    print_grouped_items(cipher, grouped_data, db)
