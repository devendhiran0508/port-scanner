"""
service_id.py
Helpers for figuring out what's likely running on an open port:
- identify_service(): static guess based on well-known port numbers
- grab_banner(): connects fresh and reads whatever the service sends first

Note: core.py's scan_port_detailed() reuses a single socket for both the
open/closed check AND the banner read (more efficient). grab_banner() here
is kept as a standalone function so you can call it independently, e.g. to
re-check a single port without rerunning a full scan.
"""

import socket


def identify_service(port):
    """
    Returns the conventional service name for a port (e.g. 22 -> 'ssh'),
    based on the system's services database. This is a guess based on
    convention, not a guarantee of what's actually running.
    """
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


def grab_banner(target, port, timeout=1):
    """
    Opens a fresh connection to target:port and reads up to 1024 bytes.
    Many services (SSH, FTP, SMTP) announce themselves immediately;
    others (HTTP) wait for a request first and may return nothing.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "No banner received"
    except Exception:
        return "Could not grab banner"
