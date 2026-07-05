"""
syn_scan.py
"Half-open" SYN scanning using Scapy: sends only a SYN packet and reads
the response, instead of completing a full TCP handshake like core.py does.

Requires:
- scapy installed (pip install scapy)
- Administrator (Windows) or root/sudo (Mac/Linux) privileges, since raw
  packet crafting is a restricted OS-level operation
- On Windows: Npcap installed (https://npcap.com), with
  "Install Npcap in WinPcap API-compatible mode" checked during setup

Note: because no full connection is ever made, there is no banner to read
here. This trades detail for speed and a smaller network footprint.
"""

from scapy.all import sr1, send, IP, TCP


def syn_scan_port(target, port, timeout=1):
    """
    Sends a single SYN packet to target:port and interprets the response.
    Returns one of: 'open', 'closed', 'filtered'.
    """
    ip = IP(dst=target)
    syn = TCP(dport=port, flags="S")

    response = sr1(ip / syn, timeout=timeout, verbose=0)

    if response is None:
        return "filtered"  # no reply at all usually means a firewall dropped it

    if response.haslayer(TCP):
        flags = response.getlayer(TCP).flags
        if flags == 0x12:  # SYN-ACK -> port is open
            # Politely tear down the half-open connection with an RST
            rst = TCP(dport=port, flags="R", seq=response[TCP].ack)
            send(ip / rst, verbose=0)
            return "open"
        elif flags == 0x14:  # RST-ACK -> port is closed
            return "closed"

    return "filtered"


def syn_scan_range(target, start_port, end_port, timeout=1):
    """
    Runs syn_scan_port sequentially across a port range.
    (Intentionally sequential to keep this step simple; combining SYN
    scanning with threading is a good later exercise once this works.)
    Returns a list of dicts, one per OPEN port.
    """
    open_ports = []

    for port in range(start_port, end_port + 1):
        result = syn_scan_port(target, port, timeout)
        if result == "open":
            print(f"Port {port:>5} OPEN")
            open_ports.append({"port": port, "state": result})
        else:
            print(f"Port {port:>5} {result}")

    return open_ports


if __name__ == "__main__":
    target = "scanme.nmap.org"
    for port in [22, 80, 443, 8080]:
        result = syn_scan_port(target, port)
        print(f"Port {port}: {result}")
