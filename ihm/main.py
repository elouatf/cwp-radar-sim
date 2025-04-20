import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer, QObject, Signal

# simulateur temporaire
class RadarBackend(QObject):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_data)
        self.timer.start(1000)

    def send_data(self):
        snapshot = [
            {'x': 50, 'y': 100, 'callsign': 'AF123', 'fl': '350', 'status': 'normal'},
            {'x': -150, 'y': 80, 'callsign': 'BA456', 'fl': '370', 'status': 'conflict'}
        ]
        ctx = self.engine.rootObjects()[0]
        ctx.setProperty("aircraftList", snapshot)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load("ihm/RadarView.qml")
    radar_backend = RadarBackend(engine)
    sys.exit(app.exec())

