#!/usr/bin/env python3
import argparse
import requests
from tabulate import tabulate


def get_snap_info(snap_name):
    url = f"https://api.snapcraft.io/v2/snaps/info/{snap_name}?fields=revision"
    headers = {"Accept": "application/json", "Snap-Device-Series": "16"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def tabulate_snap_info(snap_info):
    rows = []
    for channel_info in snap_info["channel-map"]:
        revision = channel_info["revision"]
        channel = channel_info["channel"]
        rows.append(
            [
                revision,
                channel["architecture"],
                channel["name"],
                channel["released-at"],
                channel["risk"],
                channel["track"],
            ]
        )

    headers = ["Revision", "Architecture", "Name", "Released At", "Risk", "Track"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def main():
    parser = argparse.ArgumentParser(description="Get snap channel map")
    parser.add_argument("snap_name", help="Snap name")
    args = parser.parse_args()

    try:
        snap_info = get_snap_info(args.snap_name)
        tabulate_snap_info(snap_info)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching snap info: {e}")


if __name__ == "__main__":
    main()
