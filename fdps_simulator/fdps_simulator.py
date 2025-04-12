import socket
import time
import csv
import json
import os

HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Chosen TCP port (client must match this)

SNAPSHOT_FOLDER = 'fdps_simulator/snapshots'
TICK_INTERVAL = 1  # seconds between each snapshot

def load_snapshots():
    """Load all snapshot CSV files into memory."""
    files = sorted(f for f in os.listdir(SNAPSHOT_FOLDER) if f.endswith('.csv'))
    snapshots = []
    for filename in files:
        filepath = os.path.join(SNAPSHOT_FOLDER, filename)
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            snapshot = []
            for row in reader:
                snapshot.append({
                    'callsign': row['callsign'],
                    'x': int(row['x']),
                    'y': int(row['y']),
                    'fl': row['fl'],
                    'status': row['status']
                })
            snapshots.append(snapshot)
    return snapshots

def start_server():
    print(f"[FDPS] Loading snapshots from {SNAPSHOT_FOLDER}...")
    snapshots = load_snapshots()
    print(f"[FDPS] Loaded {len(snapshots)} snapshots.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[FDPS] Waiting for IHM radar to connect on {HOST}:{PORT}...")
        conn, addr = server_socket.accept()
        print(f"[FDPS] IHM connected from {addr}")

        with conn:
            i = 0
            while True:
                snapshot = snapshots[i]
                payload = json.dumps(snapshot).encode('utf-8')
                try:
                    conn.sendall(payload + b'\n')  # Send newline-delimited JSON
                    print(f"[FDPS] Sent snapshot #{i}")
                except BrokenPipeError:
                    print("[FDPS] Client disconnected. Exiting.")
                    break

                i = (i + 1) % len(snapshots)  # Loop forever
                time.sleep(TICK_INTERVAL)

if __name__ == "__main__":
    start_server()