"""
test_core.py
Basic tests for the connect-scan logic.
Run with: python -m pytest tests/  (or: python -m unittest discover)
"""

import socket
import threading
import time
import unittest

from scanner.core import scan_port_detailed


class TestScanPortDetailed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start a tiny local TCP server on a free port so we have a
        # guaranteed-open port to test against, without depending on
        # any real service being installed on the test machine.
        cls.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.server_socket.bind(("127.0.0.1", 0))  # 0 = let OS pick a free port
        cls.port = cls.server_socket.getsockname()[1]
        cls.server_socket.listen(1)

        def accept_loop():
            while True:
                try:
                    conn, _ = cls.server_socket.accept()
                    conn.sendall(b"TEST-BANNER\n")
                    conn.close()
                except OSError:
                    break

        cls.thread = threading.Thread(target=accept_loop, daemon=True)
        cls.thread.start()
        time.sleep(0.2)  # give the server a moment to start listening

    @classmethod
    def tearDownClass(cls):
        cls.server_socket.close()

    def test_open_port_detected(self):
        port, is_open, service, banner = scan_port_detailed("127.0.0.1", self.port)
        self.assertTrue(is_open)
        self.assertEqual(port, self.port)

    def test_closed_port_detected(self):
        # Port 1 is virtually never open on a normal machine
        port, is_open, service, banner = scan_port_detailed("127.0.0.1", 1, timeout=0.5)
        self.assertFalse(is_open)
        self.assertIsNone(service)
        self.assertIsNone(banner)


if __name__ == "__main__":
    unittest.main()
