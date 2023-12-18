import AveryLabels
from reportlab.lib.units import mm, cm
from reportlab_qrcode import QRCodeImage
import argparse

import json
import os

CONFIG_FILE = "asn/config.json"


def read_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        # create default config
        config = {
            "start_asn": 1
        }
        write_config(config)

    with open(CONFIG_FILE) as f:
        return json.load(f)


def write_config(config: dict) -> None:
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def render(c, x, y):
    global startASN
    barcode_value = f"ASN{startASN:05d}"
    startASN = startASN + 1
    
    qr = QRCodeImage(barcode_value, size=y*0.9)
    qr.drawOn(c, 1*mm, y * .05)
    c.setFont("Helvetica", 2.5*mm)
    c.drawString(y, (y - 2*mm) / 2, barcode_value)


if __name__ == "__main__":
    config = read_config()

    parser = argparse.ArgumentParser(
        description='ASN barcode generator'
    )

    parser.add_argument(
        '-s', '--start_asn',
        type=int, help='starting ASN number',
        default=config["start_asn"], required=False)
    parser.add_argument(
        '-o', '--output',
        type=str, help='output file name', required=False)
    parser.add_argument(
        '-c', '--count',
        type=int, help='number of labels to generate',
        default=140, required=False)
    parser.add_argument(
        '-p', '--profile',
        type=int, help='profile to use',
        default=4731, required=False)

    args = parser.parse_args()

    startASN = args.start_asn

    if args.output is None:
        args.output = f"asn/asn_start_{startASN:05d}.pdf"

    label = AveryLabels.AveryLabel(args.profile)
    label.open(args.output)
    label.render(render, args.count)
    label.close()

    config["start_asn"] = startASN

    print(f"Generated {args.count} labels starting at {startASN:05d} in {args.output}")

    write_config(config)
