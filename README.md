./ven# Port Scanner

A simple, educational TCP port scanner written in Python. Built step by step
to learn networking fundamentals (TCP handshakes, concurrency, service
identification) rather than to compete with tools like nmap.

## Features

- **Connect scan** — full TCP handshake, works without admin/root privileges
- **SYN scan** — half-open scan using Scapy, requires admin/root (advanced)
- **Concurrent scanning** via `ThreadPoolExecutor` (I/O-bound workload)
- **Service identification** — guesses the likely service per port
- **Banner grabbing** — reads what the service announces on connect
- **JSON/CSV export** of results

## Project structure

```
port-scanner/
├── cli.py                  # Command-line entry point
├── requirements.txt
├── scanner/
│   ├── core.py              # Connect scan logic + concurrency
│   ├── service_id.py         # Service name lookup + banner grabbing
│   ├── syn_scan.py           # Scapy-based SYN scanning
│   └── utils.py              # Port range parsing, target validation
├── output/
│   └── report_writer.py      # JSON/CSV export
├── tests/
│   └── test_core.py
└── examples/
    └── scan_localhost.py     # Example of using the package directly
```

## Setup

```bash
# From the project root
python -m venv venv

# Activate the virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows cmd:
venv\Scripts\activate.bat
# Mac/Linux:
source venv/bin/activate

# Install dependencies (only needed for SYN scan mode)
pip install -r requirements.txt
```

SYN scanning also requires **Npcap** on Windows: https://npcap.com
(check "Install Npcap in WinPcap API-compatible mode" during setup).

## Usage

```bash
# Basic connect scan
python cli.py --target 127.0.0.1 --ports 1-1024

# Custom threads/timeout
python cli.py -t scanme.nmap.org -p 1-1024 --threads 200 --timeout 1.5

# Save results
python cli.py -t 127.0.0.1 -p 1-1024 --save json
python cli.py -t 127.0.0.1 -p 1-1024 --save csv

# SYN scan (requires Administrator/root + scapy + npcap)
python cli.py -t scanme.nmap.org -p 1-100 --mode syn
```

Run `python cli.py --help` for the full list of options.

## Testing

```bash
python -m pytest tests/
```

## ⚠️ Legal / ethical use

Only scan hosts you own or have explicit permission to test. Safe targets
for practice:
- `127.0.0.1` (your own machine)
- Your own home network/router
- `scanme.nmap.org` (explicitly set up by the Nmap project for this purpose)
- Your own VMs, or labs on TryHackMe / HackTheBox

Scanning systems you don't own or have permission to test can be illegal
even without causing any damage.
