# -*- coding: utf-8 -*-

import names

def main():
    startApplication("radar")
    test.log("Radar application launched")
    radar_window = waitForObjectExists(":radarWindow")
    test.verify(radar_window is not None, "Radar window is visible")