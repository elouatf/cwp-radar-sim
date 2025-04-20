import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Shapes 1.15

Window {
    id: radarWindow
    visible: true
    width: 800
    height: 800
    title: "CWP Radar Display"
    color: "black"

    property var aircraftList: aircraftManager.aircraft

    property int centerX: width / 2
    property int centerY: height / 2
    property int radiusStep: 100
    property int maxCircles: 4
    property int maxRadius: radiusStep * maxCircles

    Canvas {
        id: radarCanvas
        anchors.fill: parent
        onPaint: {
            const ctx = getContext("2d")
            ctx.reset()
            ctx.strokeStyle = "green"
            ctx.lineWidth = 1

            // Draw concentric circles
            for (let i = 1; i <= maxCircles; i++) {
                ctx.beginPath()
                ctx.arc(radarWindow.centerX, radarWindow.centerY, i * radarWindow.radiusStep, 0, 2 * Math.PI)
                ctx.stroke()
            }

            // Cross lines
            ctx.beginPath()
            ctx.moveTo(radarWindow.centerX, 0)
            ctx.lineTo(radarWindow.centerX, height)
            ctx.moveTo(0, radarWindow.centerY)
            ctx.lineTo(width, radarWindow.centerY)
            ctx.stroke()
        }
    }

    // Distance labels (20NM, 40NM, ...)
    Repeater {
        model: maxCircles
        delegate: Text {
            text: ((index + 1) * 20) + " NM"
            color: "green"
            font.pixelSize: 14
            x: centerX + (index + 1) * radiusStep + 10
            y: centerY - 10
        }
    }

    // Angular labels (0°, 30°, ..., 330°)
    Repeater {
        model: 12
        delegate: Text {
            property real angle: index * 30
            property real radians: angle * Math.PI / 180
            text: angle + "°"
            color: "green"
            font.pixelSize: 12
            x: centerX + Math.cos(radians) * (maxRadius + 20) - width / 2
            y: centerY - Math.sin(radians) * (maxRadius + 20) - height / 2
        }
    }

    // Aircraft symbols
    Repeater {
        model: radarWindow.aircraftList
        delegate: Item {
            id: trackItem
            x: centerX + modelData.x
            y: centerY - modelData.y
            width: 1; height: 1

            Rectangle {
                width: 6; height: 6
                color: modelData.status === "conflict" ? "red" : "green"
                anchors.centerIn: parent
                radius: 3
            }

            Text {
                text: modelData.callsign + " " + modelData.fl
                color: "white"
                font.pixelSize: 14
                anchors.left: parent.right
                anchors.verticalCenter: parent.verticalCenter
                anchors.leftMargin: 5
            }
        }
    }
}