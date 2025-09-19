from flask import Flask, render_template, request, jsonify
import socket
import time

app = Flask(__name__)

# --- Configure brands with host/IP options ---
BRANDS = {
    "Bareeze": [
        ("122.129.92.25", 20000),
        ("202.59.94.86", 20000),
    ],
    "Bareeze Men": [
        ("122.129.92.26", 20000),
        ("202.59.94.92", 20000),
    ],
    "Chinyere": [
        ("122.129.92.28", 20000),
        ("202.59.94.88", 20000),
    ],
    "Minnie Minor": [
        ("122.129.92.29", 20000),
        ("202.59.94.87", 20000),
    ],
    "Rang Ja": [
        ("122.129.92.30", 20000),
        ("202.59.94.91", 20000),
    ],
    "The Entertainer": [
        ("122.129.92.32", 20000),
        ("202.59.94.93", 20000),
    ],
}

def check_port(host: str, port: int, timeout: float = 10.0):
    """Try to open a TCP connection to host:port."""
    start = time.time()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        ms = int((time.time() - start) * 1000)
        return "open", ms, None
    except socket.timeout:
        ms = int((time.time() - start) * 1000)
        return "closed", ms, "timeout"
    except ConnectionRefusedError:
        ms = int((time.time() - start) * 1000)
        return "closed", ms, "connection refused"
    except socket.gaierror as e:
        return "closed", None, f"address error ({e})"
    except Exception as e:
        # For debugging purposes, you can uncomment the next line
        # print(f"Unexpected error: {e}")
        return "closed", None, str(e)

@app.route("/")
def index():
    return render_template("index.html", brands=BRANDS)

@app.route("/check", methods=["POST"])
def do_check():
    data = request.get_json(force=True)
    host = data.get("host")
    port = data.get("port")

    # Validate inputs
    try:
        port = int(port)
    except (ValueError, TypeError):
        return jsonify(status="closed", reason="invalid port"), 400

    if not host or port <= 0 or port > 65535:
        return jsonify(status="closed", reason="invalid host or port"), 400

    status, ms, reason = check_port(host, port, timeout=10.0)

    resp = {"status": status}
    if ms is not None:
        resp["ms"] = ms
    if reason:
        resp["reason"] = reason

    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
