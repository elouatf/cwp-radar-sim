import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt
from ihm.socket_client import start_socket_listener

class RadarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CWP Radar Display")
        self.setGeometry(100, 100, 800, 800)
        self.setStyleSheet("background-color: black;")
        self.aircraft = []
        start_socket_listener(self.receive_snapshot)

    def receive_snapshot(self, snapshot):
        self.aircraft = snapshot
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() // 2, self.height() // 2
        radar_color = QColor(0, 255, 0)
        pen = QPen(radar_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.setFont(self.font())

        max_radius = min(self.width(), self.height()) // 2
        radius_step = 100
        num_circles = max_radius // radius_step

        for i in range(1, num_circles + 1):
            r = i * radius_step
            painter.drawEllipse(cx - r, cy - r, 2 * r, 2 * r)
            label = f"{i * 20} NM"
            text_rect = painter.boundingRect(0, 0, 100, 20, Qt.AlignLeft, label)
            text_x = cx + r + 5
            text_y = cy - text_rect.height() // 2
            painter.drawText(text_x, text_y, label)

        painter.drawLine(cx, 0, cx, self.height())
        painter.drawLine(0, cy, self.width(), cy)

        label_radius = max_radius + 20
        for angle in range(0, 360, 30):
            radians = math.radians(angle)
            label = f"{angle}°"
            text_x = cx + math.cos(radians) * label_radius
            text_y = cy - math.sin(radians) * label_radius
            text_rect = painter.boundingRect(0, 0, 50, 20, Qt.AlignCenter, label)
            text_x -= text_rect.width() // 2
            text_y += text_rect.height() // 2
            painter.drawText(int(text_x), int(text_y), label)

        for ac in self.aircraft:
            ax = cx + ac['x']
            ay = cy - ac['y']
            dot_color = QColor(255, 0, 0) if ac['status'].lower() == 'conflict' else QColor(0, 255, 0)
            painter.setBrush(dot_color)
            painter.setPen(QPen(dot_color))
            painter.drawEllipse(ax - 3, ay - 3, 6, 6)
            label = f"{ac['callsign']} {ac['fl']}"
            painter.drawText(ax + 8, ay - 8, label)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
