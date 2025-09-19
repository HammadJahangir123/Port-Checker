import socket
import time

def check_port(host, port, timeout=5):
    start = time.time()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        ms = int((time.time() - start) * 1000)
        print(f"{host}:{port} is OPEN, took {ms}ms")
    except Exception as e:
        ms = int((time.time() - start) * 1000)
        print(f"{host}:{port} is CLOSED or unreachable. Reason: {e} (took {ms}ms)")

# Test Google DNS port 53 (almost always open)
check_port("8.8.8.8", 53)
check_port("google.com", 443)  # HTTPS
check_port("yahoo.com", 443)