import socket
import json
import threading
import time
import http.client
from pathlib import Path

MAPPING_FILE = Path("/var/www/codethinkers-staging/project_ports.json")
DJANGO_SOCKET = "/var/www/codethinkers-staging/codethinkers-staging.sock"

_waking_lock = threading.Lock()
_waking_in_progress = {}


class UnixSocketHTTPConnection(http.client.HTTPConnection):
    """HTTPConnection subclass that connects over a Unix domain socket
    instead of TCP — lets us call the internal wake endpoint without
    opening a new port, consistent with how gunicorn is already exposed."""
    def __init__(self, socket_path, timeout=15):
        super().__init__("localhost", timeout=timeout)
        self.socket_path = socket_path

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(self.socket_path)


def get_entry(host):
    """Extract subdomain and look up its mapping entry.
    Tolerates the old bare-int format so a stale mapping file never
    breaks the router — it just can't wake that specific entry until
    the project is rebuilt through the normal flow, which refreshes
    it to the new format automatically."""
    subdomain = host.split('.')[0]
    if MAPPING_FILE.exists():
        try:
            mapping = json.loads(MAPPING_FILE.read_text())
            entry = mapping.get(subdomain)
            if isinstance(entry, int):
                entry = {"port": entry, "project_id": None}
            return subdomain, entry
        except json.JSONDecodeError:
            pass
    return subdomain, None


def wake_project(subdomain):
    """Ask Django to start the project's server, over the internal Unix
    socket. If another thread is already waking this same subdomain,
    wait for it instead of triggering a duplicate start."""
    with _waking_lock:
        if subdomain in _waking_in_progress:
            event = _waking_in_progress[subdomain]
            already_waking = True
        else:
            event = threading.Event()
            _waking_in_progress[subdomain] = event
            already_waking = False

    if already_waking:
        event.wait(timeout=20)
        _, entry = get_entry(f"{subdomain}.codethinkers.org")
        return entry.get("port") if entry else None

    result = None
    try:
        conn = UnixSocketHTTPConnection(DJANGO_SOCKET, timeout=15)
        conn.request(
            "POST",
            f"/webprojects/internal/wake/{subdomain}/",
            headers={"Host": "staging.codethinkers.org"},
        )
        resp = conn.getresponse()
        data = json.loads(resp.read())
        conn.close()
        if data.get("status") == "success":
            result = data.get("port")
    except Exception as e:
        print(f"Wake request failed for {subdomain}: {e}")
    finally:
        with _waking_lock:
            del _waking_in_progress[subdomain]
        event.set()

    return result


def try_connect(port, retries=15, delay=1):
    """Poll until the backend port accepts connections, or give up."""
    for _ in range(retries):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(('127.0.0.1', port))
            return s
        except (ConnectionRefusedError, socket.timeout, OSError):
            time.sleep(delay)
    return None


def proxy(client_sock):
    try:
        request = client_sock.recv(8192)
        if not request:
            return

        host = None
        for line in request.decode(errors='ignore').split('\r\n'):
            if line.lower().startswith('host:'):
                host = line.split(':')[1].strip()
                break
        if not host:
            return

        subdomain, entry = get_entry(host)
        port = entry.get("port") if entry else None

        backend = try_connect(port, retries=1) if port else None
    
        if not backend:
            if not entry:
                resp = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nProject not found"
                client_sock.send(resp)
                return

            if not entry.get("project_id"):
                resp = (
                    b"HTTP/1.1 503 Service Unavailable\r\n"
                    b"Content-Type: text/plain\r\n\r\n"
                    b"This project needs to be reopened once in the editor to enable "
                    b"auto-start. After that, this link will always work."
                )
                client_sock.send(resp)
                return

            new_port = wake_project(subdomain)
            if not new_port:
                resp = b"HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/plain\r\n\r\nCould not start project"
                client_sock.send(resp)
                return

            backend = try_connect(new_port, retries=15, delay=1)
            if not backend:
                resp = b"HTTP/1.1 504 Gateway Timeout\r\nContent-Type: text/plain\r\n\r\nProject is starting, please refresh in a few seconds"
                client_sock.send(resp)
                return

        backend.send(request)
        while True:
            try:
                data = backend.recv(8192)
                if not data:
                    break
                client_sock.send(data)
            except socket.timeout:
                break
        backend.close()

    except Exception as e:
        try:
            resp = b"HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/plain\r\n\r\nProxy error"
            client_sock.send(resp)
        except Exception:
            pass
        print(f"Proxy error: {e}")
    finally:
        client_sock.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 9000))
    server.listen(50)
    print("Router listening on port 9000")
    while True:
        client, _ = server.accept()
        threading.Thread(target=proxy, args=(client,), daemon=True).start()


if __name__ == '__main__':
    main()