import sys
from PySide6.QtWidgets import QApplication
from ihm.radar_widget import RadarWidget

def main():
    app = QApplication(sys.argv)
    radar = RadarWidget()
    radar.showFullScreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
