import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from ihm.aircraft_model import AircraftManager
from ihm.socket_client import start_socket_listener

def main():
    app = QApplication(sys.argv)

    # Bridge Python → QML
    manager = AircraftManager()

    # Lancement du socket (données dynamiques)
    start_socket_listener(manager.update_aircraft)

    # Setup QML engine
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("aircraftManager", manager)
    engine.load("ihm/RadarView.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()