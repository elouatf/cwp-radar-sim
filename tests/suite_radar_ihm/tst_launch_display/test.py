# -*- coding: utf-8 -*-

import names

def main():
    startApplication("radar")
    test.log("Radar application launched")
    radar_window = waitForObjectExists(":radarWidget")
    test.verify(radar_window is not None, "Radar widget is visible")