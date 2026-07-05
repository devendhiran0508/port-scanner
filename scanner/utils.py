"""
utils.py
Small helper functions used across the scanner package:
- parsing CLI input like "1-1024" into integers
- validating that a target hostname/IP resolves before we try to scan it
"""

import socket


def parse_port_range(port_string):
    """
    Converts a string like '1-1024' or '80' into (start, end) integers.
    Raises ValueError if the format or range is invalid.
    """
    port_string = port_string.strip()

    if "-" in port_string:
        start_str, end_str = port_string.split("-", 1)
        start, end = int(start_str), int(end_str)
    else:
        start = end = int(port_string)

    if start < 1 or end > 65535:
        raise ValueError("Ports must be between 1 and 65535")
    if start > end:
        raise ValueError("Start port cannot be greater than end port")

    return start, end


def resolve_target(target):
    """
    Confirms the target hostname/IP can be resolved.
    Returns the resolved IP address, or raises ValueError with a clear message.
    """
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        raise ValueError(f"Could not resolve host: {target}")
