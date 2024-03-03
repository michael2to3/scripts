#!/usr/bin/python3
from typing import NoReturn
import argparse
import sys
import xml.etree.ElementTree as ET


def parse_nmap_xml(xml_input: str) -> NoReturn:
    root = ET.fromstring(xml_input)
    for host in root.findall(".//host"):
        domain = None

        hostnames = host.find(".//hostnames")
        if hostnames is not None:
            hostname_element = hostnames.find(".//hostname")
            if hostname_element is not None:
                domain = hostname_element.get("name")

        if domain is None:
            address_element = host.find(".//address")
            if address_element is not None:
                domain = address_element.get("addr")

        if domain:
            ports = host.find(".//ports")
            if ports is not None:
                for port in ports.findall(".//port"):
                    state = port.find(".//state")
                    if state is not None and state.get("state") == "open":
                        portid = port.get("portid")
                        print(f"{domain}:{portid}")


def main() -> NoReturn:
    parser = argparse.ArgumentParser(
        description="Parse nmap XML and output in DOMAIN:PORT format."
    )
    args = parser.parse_args()

    xml_input = sys.stdin.read()
    parse_nmap_xml(xml_input)


if __name__ == "__main__":
    main()
