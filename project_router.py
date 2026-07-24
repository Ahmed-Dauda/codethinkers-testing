import socket
import json
from pathlib import Path

MAPPING_FILE = Path("/var/www/codethinkers-staging/project_ports.json")

def get_port(host):
    """Extract subdomain and look up port."""
    subdomain = host.split('.')[0]
    if MAPPING_FILE.exists():
        mapping = json.loads(MAPPING_FILE.read_text())
        return mapping.get(subdomain)
    return None

def proxy(client_sock):
    request = client_sock.recv(8192)
    if not request:
        client_sock.close()
        return

    # Extract host header
    host = None
    for line in request.decode(errors='ignore').split('\r\n'):
        if line.lower().startswith('host:'):
            host = line.split(':')[1].strip()
            break

    if not host:
        client_sock.close()
        return

    port = get_port(host)

    if not port:
        resp = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nProject not found"
        client_sock.send(resp)
        client_sock.close()
        return

    try:
        backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend.settimeout(30)
        backend.connect(('127.0.0.1', port))
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
    except Exception:
        resp = b"HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/plain\r\n\r\nProject not running"
        client_sock.send(resp)
    finally:
        client_sock.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 9000))
    server.listen(20)
    print("Router listening on port 9000")

    while True:
        client, _ = server.accept()
        proxy(client)

if __name__ == '__main__':
    main()
