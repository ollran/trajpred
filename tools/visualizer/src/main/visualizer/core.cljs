;;;; Visualization tool

;;;; - https://shadow-cljs.org/
;;;;     shadow-cljs provides everything you need
;;;;     to compile your ClojureScript code with a
;;;;     focus on simplicity and ease of use.
;;;;
;;;; - https://leafletjs.com/
;;;;     an open-source JavaScript library
;;;;     for mobile-friendly interactive maps.

(ns visualizer.core
  (:require [clojure.string :as str]))

(def L
  js/L)

(defonce L-map
  (.map L "mapid"))

(defonce polygon-layer-group
  (.layerGroup L))

(def tilelayer-settings
  (js-obj "maxZoom" 19
          "attribution" "&copy; <a href=\"https://openstreetmap.org/copyright\">OpenStreetMap contributors</a>"))

(def colors
  ["black" "blue" "red"])

(defn parse-input [input]
  (as-> input i
    (str/split i "---")
    (map #(str/split % "\n") i)
    (map (fn [n] (map (fn [m] (str/split m ",")) n)) i)
    (map (fn [n] (filter (fn [m] (> (count m) 1))  n)) i)
    (map (fn [n] (map (fn [m] (apply array m)) n)) i)
    (map #(apply array %) i)))

(defn draw-path [path color]
  (let [polyline (.polyline L path (js-obj "color" color))
        bounds (.getBounds polyline)]
    (.addLayer polygon-layer-group polyline)
    (.addTo polygon-layer-group L-map)
    (.fitBounds L-map bounds)))

(defn init []
  (let [l-tilelayer (.tileLayer L "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" tilelayer-settings)
        l-scale (.control.scale L)]
    (.setView L-map (array 62.601090 29.763530) 13)
    (.addTo l-tilelayer L-map)
    (.addTo l-scale L-map)))

(defn ^:export draw []
  (let [input (-> js/document
                  (.getElementById "input")
                  (.-value))
        parsed-input (parse-input input)]
    (doseq [[path color]
            (map list parsed-input colors)]
      (when (not-empty path)
        (draw-path path color)))))

(defn ^:export clear []
  (.remove polygon-layer-group)
  (.clearLayers polygon-layer-group))
