import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QTimer

class RadarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CWP Radar Display")
        self.setGeometry(100, 100, 800, 800)  # Can be full screen if needed
        self.setStyleSheet("background-color: black;")

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

        # Draw concentric circles
        max_radius = min(self.width(), self.height()) // 2
        radius_step = 100  # Change later to simulate zoom
        num_circles = max_radius // radius_step

        for i in range(1, num_circles + 1):
            painter.drawEllipse(
                cx - i * radius_step,
                cy - i * radius_step,
                2 * i * radius_step,
                2 * i * radius_step
            )

        # Draw cross lines
        painter.drawLine(cx, 0, cx, self.height())  # vertical
        painter.drawLine(0, cy, self.width(), cy)  # horizontal

        # # Optional: angle lines (like 45°)
        # painter.save()
        # for angle in range(0, 360, 30):
        #     painter.rotate(angle)
        #     painter.drawLine(cx, cy, cx, cy - 400)
        #     painter.resetTransform()
        # painter.restore()

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