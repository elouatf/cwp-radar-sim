import socket
import threading
import json
from ihm.config import FDPS_HOST, FDPS_PORT

def start_socket_listener(on_update):
    def listen():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((FDPS_HOST, FDPS_PORT))
                buffer = b''
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    buffer += data
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        try:
                            snapshot = json.loads(line.decode('utf-8'))
                            on_update(snapshot)
                        except json.JSONDecodeError as e:
                            print(f"[Radar] JSON decode error: {e}")
        except ConnectionRefusedError:
            print("[Radar] Could not connect to FDPS simulator (localhost:5000)")

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
