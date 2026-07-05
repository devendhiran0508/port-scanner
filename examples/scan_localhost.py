"""
scan_localhost.py
Example of using the scanner package directly in Python code,
instead of through the CLI. Run from the project root:

    python examples/scan_localhost.py
"""

import sys
import os

# Allow this script to find the 'scanner' package when run directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scanner.core import scan_range_concurrent

if __name__ == "__main__":
    results = scan_range_concurrent(
        target="127.0.0.1",
        start_port=1,
        end_port=1024,
        timeout=1,
        max_threads=200
    )
    print("\nOpen ports summary:")
    for r in results:
        print(r)
