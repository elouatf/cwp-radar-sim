from PySide6.QtCore import QObject, Signal, Slot, Property

class AircraftManager(QObject):
    aircraftChanged = Signal(list)

    def __init__(self):
        super().__init__()
        self._aircraft = []

    @Slot(list)
    def update_aircraft(self, new_list):
        self._aircraft = new_list
        self.aircraftChanged.emit(self._aircraft)

    @Property('QVariantList', notify=aircraftChanged)
    def aircraft(self):
        return self._aircraft
