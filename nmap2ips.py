from typing import NoReturn
import argparse
import sys
import xml.etree.ElementTree as ET


def parse_nmap_xml(xml_input: str) -> NoReturn:
    root = ET.fromstring(xml_input)
    for host in root.findall(".//host"):
        hostnames = host.find(".//hostnames")
        if hostnames is not None:
            for hostname in hostnames.findall(".//hostname"):
                domain = hostname.get("name")
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
