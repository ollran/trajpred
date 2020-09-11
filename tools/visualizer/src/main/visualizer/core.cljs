(ns visualizer.core)

(def L js/L)

(def tilelayer-settings
  (js-obj "maxZoom" 19
          "attribution" "&copy; <a href=\"https://openstreetmap.org/copyright\">OpenStreetMap contributors</a>"))

(defn init []
  (let [l-map (.map L "mapid")
        l-tilelayer (.tileLayer L "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" tilelayer-settings)]
    (.setView l-map (array 62.601090 29.763530) 13)
    (.addTo l-tilelayer l-map)))
