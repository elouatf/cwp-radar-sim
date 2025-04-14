# -*- coding: utf-8 -*-

import names

def main():
    startApplication("radar")
    test.log("Radar application launched")
    radar = waitForObjectExists(":radarWidget")
    test.verify(radar is not None, "Radar widget is visible")