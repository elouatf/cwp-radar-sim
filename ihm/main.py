import sys
import math
import csv
import socket
import threading
import json
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QTimer

class RadarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CWP Radar Display")
        self.setGeometry(100, 100, 800, 800)  # Can be full screen if needed
        self.setStyleSheet("background-color: black;")
        self.aircraft = []  # Starts empty
        self.start_socket_client()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Center of radar
        cx, cy = self.width() // 2, self.height() // 2

        # Radar color
        radar_color = QColor(0, 255, 0)  # Green

        # Pen settings
        pen = QPen(radar_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.setFont(self.font())  # Use default font

        # Draw concentric circles
        max_radius = min(self.width(), self.height()) // 2
        radius_step = 100  # Change later to simulate zoom
        num_circles = max_radius // radius_step

        for i in range(1, num_circles + 1):
            r = i * radius_step
            painter.drawEllipse(cx - r, cy - r, 2 * r,2 * r)
            # Draw a range label (e.g., "20 NM") on the right side of the circle
            label = f"{i * 20} NM"  # Assuming each ring = 20 NM
            text_rect = painter.boundingRect(0, 0, 100, 20, Qt.AlignLeft, label)
            text_x = cx + r + 5
            text_y = cy - text_rect.height() // 2
            painter.drawText(text_x, text_y, label)

        # Draw cross lines
        painter.drawLine(cx, 0, cx, self.height())  # vertical
        painter.drawLine(0, cy, self.width(), cy)  # horizontal
        
        # Draw angle lines (every 30°, like compass spokes)
        label_radius = max_radius + 20  # Put the label slightly outside the last ring

        for angle in range(0, 360, 30):
            radians = math.radians(angle)
            label = f"{angle}°"

            text_x = cx + math.cos(radians) * label_radius
            text_y = cy - math.sin(radians) * label_radius

            text_rect = painter.boundingRect(0, 0, 50, 20, Qt.AlignCenter, label)
            text_x -= text_rect.width() // 2
            text_y += text_rect.height() // 2

            painter.drawText(int(text_x), int(text_y), label)
        
        # Draw aircraft on top of radar
        for ac in self.aircraft:
            ax = cx + ac['x']
            ay = cy - ac['y']  # y-axis reversed (Qt origin is top-left)

            # Dot representing the aircraft
            # Set color depending on aircraft status
            if ac['status'].lower() == 'conflict':
                dot_color = QColor(255, 0, 0)  # Red
            else:
                dot_color = QColor(0, 255, 0)  # Green
            painter.setBrush(dot_color)
            painter.setPen(QPen(dot_color))  # Optional: match dot and label color
            painter.drawEllipse(ax - 3, ay - 3, 6, 6)

            # Label: callsign + FL
            label = f"{ac['callsign']} {ac['fl']}"
            painter.drawText(ax + 8, ay - 8, label)

    def start_socket_client(self):
        def listen():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('127.0.0.1', 5000))
                    buffer = b''
                    while True:
                        data = s.recv(4096)
                        if not data:
                            break
                        buffer += data

                        # Handle full JSON message (newline-delimited)
                        while b'\n' in buffer:
                            line, buffer = buffer.split(b'\n', 1)
                            try:
                                snapshot = json.loads(line.decode('utf-8'))
                                self.aircraft = snapshot
                                self.update()
                            except json.JSONDecodeError as e:
                                print(f"[Radar] JSON decode error: {e}")

            except ConnectionRefusedError:
                print("[Radar] Could not connect to FDPS simulator (localhost:5000)")

        # Run the socket client in a separate thread
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # Quit the app on Esc


def main():
    app = QApplication(sys.argv)
    radar = RadarWidget()
    radar.showFullScreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()