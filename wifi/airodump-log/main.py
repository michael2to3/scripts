import argparse
import csv
import sys


def parse_airodump_csv(filename):
    with open(filename, "r", encoding="utf-8", errors="ignore") as csvfile:
        ap_list = []
        client_section = False
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            if row[0].strip() == "Station MAC":
                client_section = True
                continue
            if client_section:
                continue
            else:
                bssid = row[0].strip()
                first_time_seen = row[1].strip()
                last_time_seen = row[2].strip()
                channel = row[3].strip()
                speed = row[4].strip()
                privacy = row[5].strip()
                cipher = row[6].strip()
                authentication = row[7].strip()
                power = row[8].strip()
                nb_packets = row[9].strip()
                nb_beacons = row[10].strip()
                data = row[11].strip()
                lan_ip = row[12].strip()
                id_length = row[13].strip()
                essid = row[13].strip()

                ap_info = {
                    "bssid": bssid,
                    "essid": essid,
                    "clients": int(nb_packets) if nb_packets.isdigit() else 0,
                    "power": int(power) if power.lstrip("-").isdigit() else 0,
                    "first_time_seen": first_time_seen,
                    "last_time_seen": last_time_seen,
                }
                ap_list.append(ap_info)
        return ap_list


def main():
    parser = argparse.ArgumentParser(description="Process airodump-ng CSV file.")
    parser.add_argument("filename", help="The CSV file to process")
    parser.add_argument(
        "--sort", default="clients", help="Sorting criteria (comma-separated)"
    )
    args = parser.parse_args()

    ap_list = parse_airodump_csv(args.filename)

    sort_keys = {
        "clients": "clients",
        "power": "power",
        "first_seen": "first_time_seen",
        "last_seen": "last_time_seen",
        "essid": "essid",
        "bssid": "bssid",
    }

    sort_criteria = []
    for key in args.sort.split(","):
        key = key.strip()
        if key in sort_keys:
            sort_criteria.append(sort_keys[key])
        else:
            print(f"Unknown sorting key: {key}")
            sys.exit(1)

    def sort_function(ap):
        sort_values = []
        for criterion in sort_criteria:
            value = ap[criterion]
            if isinstance(value, str):
                sort_values.append(value)
            else:
                sort_values.append(-value)
        return tuple(sort_values)

    ap_list.sort(key=sort_function)

    print(f"{'ESSID':<20} {'BSSID':<20} {'Clients':<7} {'Power':<5}")
    print("-" * 60)
    for ap in ap_list:
        print(
            f"{ap['essid']:<20} {ap['bssid']:<20} {ap['clients']:<7} {ap['power']:<5}"
        )


if __name__ == "__main__":
    main()
