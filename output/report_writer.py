"""
report_writer.py
Saves scan results (a list of dicts, as returned by scan_range_concurrent)
to disk as JSON or CSV, so results can be kept, diffed over time, or
imported into other tools/spreadsheets.
"""

import json
import csv
import os
from datetime import datetime


def save_json(results, target, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"scan_{target}_{timestamp}.json")

    report = {
        "target": target,
        "timestamp": timestamp,
        "open_ports": results
    }

    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report saved to {filename}")
    return filename


def save_csv(results, target, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"scan_{target}_{timestamp}.csv")

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["port", "service", "banner"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Report saved to {filename}")
    return filename
