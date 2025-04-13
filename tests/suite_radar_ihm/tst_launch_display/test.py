# -*- coding: utf-8 -*-

import names

def main():
    startApplication("radar.sh")
    test.log("Radar application launched")
    waitForObjectExists(":RadarWidget")
    test.verify(object.exists(":RadarWidget"), "Radar widget is visible")