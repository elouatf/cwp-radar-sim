# -*- coding: utf-8 -*-

import names

def main():
    # 1. Start the application
    startApplication("radar")
    test.log("Radar application launched.")

    # 2. Wait for the radar main window
    radar_window = waitForObjectExists(":radarWidget")
    test.verify(radar_window is not None, "Radar main window is visible.")

    # 3. Wait for the first aircraft track
    aircraft_symbol = waitForObjectExists("{type='QQuickItem' name='track_AF123_symbol'}")
    test.verify(aircraft_symbol is not None, "Aircraft symbol is visible")
#    aircraft_label = waitForObjectExists("{type='QQuickItem' visible='1' name~='track_.*'}")
#    test.verify(aircraft_label is not None, "Aircraft track is visible.")

    # 4. Extract displayed values (example: callsign or altitude)
#    displayed_text = str(aircraft_label.text)  # may vary depending on your widget
#    test.log("Displayed aircraft text: " + displayed_text)

    # 5. Compare with known test data (example: from a known test input)
#    expected_text = "AF123  35000 ft"  # replace with your expected label content
#    test.verify(expected_text in displayed_text, f"Displayed data matches test input: {expected_text}")