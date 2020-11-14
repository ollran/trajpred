import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtLocation 5.6
import QtPositioning 5.6

ApplicationWindow {
    visible: true
    width: 960
    height: 720
    title: qsTr("Trajectory Visualizer")

    Plugin {
        id: mapboxglPlugin
        name: "mapboxgl"
    }

    Map {
        anchors.fill: parent
        plugin: mapboxglPlugin
        center: QtPositioning.coordinate(62.601090, 29.763530)
        zoomLevel: 14
    }
}
