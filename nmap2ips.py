#!/usr/bin/python3
import argparse
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PortInfo:
    domain: str
    portid: str


class NmapXMLParser:
    def __init__(self, xml_input: str, use_hostname: bool):
        self.xml_input = xml_input
        self.use_hostname = use_hostname

    def parse(self) -> List[PortInfo]:
        root = ET.fromstring(self.xml_input)
        results = []
        for host in root.findall(".//host"):
            domain = self._get_domain(host)
            if domain:
                results.extend(self._get_open_ports(domain, host))
        return results

    def _get_domain(self, host: ET.Element) -> Optional[str]:
        if self.use_hostname:
            hostname_element = host.find(".//hostnames//hostname")
            if hostname_element is not None:
                return hostname_element.get("name")

        address_element = host.find(".//address")
        if address_element is not None:
            return address_element.get("addr")

        return None

    def _get_open_ports(self, domain: str, host: ET.Element) -> List[PortInfo]:
        ports_info = []
        for port in host.findall(".//ports//port"):
            state = port.find(".//state")
            if state is not None and state.get("state") == "open":
                portid = port.get("portid")
                ports_info.append(PortInfo(domain, portid))
        return ports_info


def print_ports(ports: List[PortInfo]) -> None:
    for port in ports:
        print(f"{port.domain}:{port.portid}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse nmap XML and output in DOMAIN:PORT format."
    )
    parser.add_argument(
        "-n", action="store_false", help="Do not use hostname", dest="use_hostname"
    )
    args = parser.parse_args()

    xml_input = sys.stdin.read()
    parser = NmapXMLParser(xml_input, args.use_hostname)
    port_info = parser.parse()
    print_ports(port_info)


if __name__ == "__main__":
    main()
