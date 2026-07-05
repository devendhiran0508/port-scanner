"""
core.py
The main TCP "connect scan" logic:
- scan_port_detailed(): checks a single port and, if open, grabs the
  service guess + banner using the SAME socket (no duplicate connection)
- scan_range_concurrent(): runs scan_port_detailed across a port range
  using a thread pool, since scanning is I/O-bound (mostly waiting on
  the network, not the CPU) and threads overlap nicely during that wait
"""

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from scanner.service_id import identify_service


def scan_port_detailed(target, port, timeout=1):
    """
    Attempts a full TCP connection to target:port.
    Returns a tuple: (port, is_open, service, banner)
    service/banner are None if the port is closed.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((target, port))

    if result == 0:
        service = identify_service(port)
        try:
            banner = sock.recv(1024).decode(errors="ignore").strip()
            banner = banner if banner else "No banner received"
        except Exception:
            banner = "Could not grab banner"
        sock.close()
        return port, True, service, banner

    sock.close()
    return port, False, None, None


def scan_range_concurrent(target, start_port, end_port, timeout=1, max_threads=100):
    """
    Scans every port in [start_port, end_port] concurrently.
    Returns a list of dicts, one per OPEN port, sorted by port number.
    """
    open_ports = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(scan_port_detailed, target, port, timeout)
            for port in range(start_port, end_port + 1)
        ]

        for future in as_completed(futures):
            port, is_open, service, banner = future.result()
            if is_open:
                print(f"Port {port:>5} OPEN   service={service:<15} banner={banner}")
                open_ports.append({
                    "port": port,
                    "service": service,
                    "banner": banner
                })

    elapsed = time.time() - start_time
    print(f"\nScan completed in {elapsed:.2f} seconds. "
          f"{len(open_ports)} open port(s) found out of {end_port - start_port + 1} scanned.")

    return sorted(open_ports, key=lambda p: p["port"])
