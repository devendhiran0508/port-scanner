"""
cli.py
Command-line entry point for the port scanner.
Handles argument parsing and output only — all scanning logic lives in
the scanner/ package, and reporting logic lives in output/report_writer.py.

Examples:
    python cli.py --target 127.0.0.1 --ports 1-1024
    python cli.py -t scanme.nmap.org -p 20-25 --threads 200 --save json
    python cli.py -t scanme.nmap.org -p 1-100 --mode syn
"""

import argparse
import sys

from scanner.core import scan_range_concurrent
from scanner.utils import parse_port_range, resolve_target
from output.report_writer import save_json, save_csv


def main():
    parser = argparse.ArgumentParser(
        description="A simple TCP port scanner for learning purposes."
    )
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Target IP address or hostname (e.g., scanme.nmap.org)"
    )
    parser.add_argument(
        "--ports", "-p",
        default="1-1024",
        help="Port range to scan, e.g. '1-1024' or '80' (default: 1-1024)"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=100,
        help="Number of concurrent threads for connect scans (default: 100)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Socket timeout in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--mode",
        choices=["connect", "syn"],
        default="connect",
        help="Scan mode: 'connect' (default, full handshake, works without "
             "admin rights) or 'syn' (requires admin/root + scapy + npcap)"
    )
    parser.add_argument(
        "--save",
        choices=["json", "csv"],
        help="Save results to output/ in the given format (connect mode only)"
    )

    args = parser.parse_args()

    # Validate port range input early, with a clear error message
    try:
        start_port, end_port = parse_port_range(args.ports)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Confirm the target actually resolves before attempting to scan it
    try:
        resolved_ip = resolve_target(args.target)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Scanning {args.target} ({resolved_ip}) "
          f"ports {start_port}-{end_port} in '{args.mode}' mode...\n")

    if args.mode == "connect":
        results = scan_range_concurrent(
            target=args.target,
            start_port=start_port,
            end_port=end_port,
            timeout=args.timeout,
            max_threads=args.threads
        )

        if args.save == "json":
            save_json(results, args.target)
        elif args.save == "csv":
            save_csv(results, args.target)

    else:  # syn mode
        # Imported here, not at the top of the file, so that users who
        # only want connect scans don't need scapy/npcap installed at all
        from scanner.syn_scan import syn_scan_range
        syn_scan_range(args.target, start_port, end_port, timeout=args.timeout)


if __name__ == "__main__":
    main()
