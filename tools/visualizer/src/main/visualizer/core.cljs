(ns visualizer.core
  (:require [clojure.string :as str]))

(def L js/L)

(defonce L-map (.map L "mapid"))

(def tilelayer-settings
  (js-obj "maxZoom" 19
          "attribution" "&copy; <a href=\"https://openstreetmap.org/copyright\">OpenStreetMap contributors</a>"))

(def polygon-layer-group (.layerGroup L))

(defn init []
  (let [l-tilelayer (.tileLayer L "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" tilelayer-settings)
        l-scale (.control.scale L)]
    (.setView L-map (array 62.601090 29.763530) 13)
    (.addTo l-tilelayer L-map)
    (.addTo l-scale L-map)))

(defn parse-raw-input [raw-input]
  (as-> raw-input i
    (str/split i "\n")
    (map #(str/split % ",") i)
    (filter #(> (count %) 1) i)
    (map #(apply array %) i)
    (apply array i)))

(defn draw-path [path color]
  (let [polyline (.polyline L path (js-obj "color" color))
        bounds (.getBounds polyline)]
    (.addLayer polygon-layer-group polyline)
    (.addTo polygon-layer-group L-map)
    (.fitBounds L-map bounds)))

(defn ^:export add [id]
  (let [raw-input (-> js/document
                      (.getElementById id)
                      (.-value))
        parsed-input (parse-raw-input raw-input)
        color (cond (= id "head") "black"
                    (= id "tail") "blue"
                    (= id "pred") "red")]
    (when (not-empty parsed-input)
      (draw-path parsed-input color))))

(defn ^:export clear-all []
  (.remove polygon-layer-group)
  (.clearLayers polygon-layer-group))
