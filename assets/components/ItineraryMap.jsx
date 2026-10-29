import { useEffect, useRef } from "react";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

maplibregl.setWorkerUrl(
  `/static/maplibre/maplibre-gl-worker.mjs?v=${maplibregl.getVersion()}`,
);

const FALLBACK_CENTER = [-2.2431, 51.8642];

/** Check longitude/latitude values before passing them to MapLibre. */
const isValidCoordinate = (lng, lat) => {
  const x = Number(lng);
  const y = Number(lat);

  return (
    lng != null &&
    lat != null &&
    Number.isFinite(x) &&
    Number.isFinite(y) &&
    x >= -180 &&
    x <= 180 &&
    y >= -90 &&
    y <= 90
  );
};

/** Convert valid map points into the GeoJSON format used by MapLibre sources. */
const toFeatureCollection = (items = []) => ({
  type: "FeatureCollection",
  features: items
    .filter((item) => isValidCoordinate(item.lng, item.lat))
    .map((item) => ({
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [Number(item.lng), Number(item.lat)],
      },
      properties: {
        id: String(item.id ?? ""),
        name: String(item.name ?? "Unnamed location"),
      },
    })),
});

// Show scheduled stops separately so they can be styled and filtered independently.
function syncSources(map, stops, attractions) {
  const scheduledIds = new Set(
    stops
      .filter((stop) => stop.attractionId != null)
      .map((stop) => String(stop.attractionId)),
  );

  const availableAttractions = attractions.filter(
    (attraction) => !scheduledIds.has(String(attraction.id)),
  );

  map.getSource("stops")?.setData(toFeatureCollection(stops));
  map
    .getSource("attractions")
    ?.setData(toFeatureCollection(availableAttractions));
}

/** Frame all scheduled stops, or fall back to the destination when none exist. */
function fitView(map, stops, center) {
  const validStops = stops.filter((stop) =>
    isValidCoordinate(stop.lng, stop.lat),
  );

  if (validStops.length > 1) {
    const bounds = new maplibregl.LngLatBounds();
    validStops.forEach((stop) =>
      bounds.extend([Number(stop.lng), Number(stop.lat)]),
    );
    map.fitBounds(bounds, { padding: 60, maxZoom: 14, duration: 500 });
  } else if (validStops.length === 1) {
    map.easeTo({
      center: [Number(validStops[0].lng), Number(validStops[0].lat)],
      zoom: 13,
      duration: 500,
    });
  } else if (isValidCoordinate(center?.lng, center?.lat)) {
    map.easeTo({
      center: [Number(center.lng), Number(center.lat)],
      zoom: 11,
      duration: 500,
    });
  }
}

/** Display available attractions and scheduled stops on an interactive map. */
export default function ItineraryMap({ center, stops = [], attractions = [] }) {
  const containerRef = useRef(null);
  const mapRef = useRef(null);
  const readyRef = useRef(false);

  const dataRef = useRef({ center, stops, attractions });
  // Keep the latest props available to the map's one-time load callback.
  dataRef.current = { center, stops, attractions };

  const stopsKey = JSON.stringify(stops);
  const attractionsKey = JSON.stringify(attractions);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const initialCenter = isValidCoordinate(
      dataRef.current.center?.lng,
      dataRef.current.center?.lat,
    )
      ? [Number(dataRef.current.center.lng), Number(dataRef.current.center.lat)]
      : FALLBACK_CENTER;

    const map = new maplibregl.Map({
      container: containerRef.current,
      style: "https://tiles.openfreemap.org/styles/liberty",
      center: initialCenter,
      zoom: 11,
    });

    mapRef.current = map;

    map.addControl(new maplibregl.NavigationControl(), "top-right");

    map.on("error", (e) => console.error("Map error:", e.error));

    const handleLoad = () => {
      if (mapRef.current !== map) return;

      map.addSource("attractions", {
        type: "geojson",
        data: toFeatureCollection([]),
      });

      map.addLayer({
        id: "attractions-layer",
        type: "circle",
        source: "attractions",
        paint: {
          "circle-radius": 7,
          "circle-color": "#ef4444",
          "circle-stroke-width": 2,
          "circle-stroke-color": "#ffffff",
        },
      });

      map.addSource("stops", {
        type: "geojson",
        data: toFeatureCollection([]),
      });

      map.addLayer({
        id: "stops-layer",
        type: "circle",
        source: "stops",
        paint: {
          "circle-radius": 9,
          "circle-color": "#2563eb",
          "circle-stroke-width": 2,
          "circle-stroke-color": "#ffffff",
        },
      });

      ["attractions-layer", "stops-layer"].forEach((layerId) => {
        // Share popup and hover behavior between the two point layers.
        map.on("click", layerId, (event) => {
          const feature = event.features?.[0];
          if (!feature) return;

          new maplibregl.Popup()
            .setLngLat(feature.geometry.coordinates.slice())
            .setText(feature.properties?.name || "Location")
            .addTo(map);
        });

        map.on("mouseenter", layerId, () => {
          map.getCanvas().style.cursor = "pointer";
        });

        map.on("mouseleave", layerId, () => {
          map.getCanvas().style.cursor = "";
        });
      });

      readyRef.current = true;

      const data = dataRef.current;
      syncSources(map, data.stops, data.attractions);
      fitView(map, data.stops, data.center);
    };

    map.on("load", handleLoad);

    const observer = new ResizeObserver(() => {
      if (!mapRef.current) return;
      map.resize();
    });

    observer.observe(containerRef.current);

    return () => {
      observer.disconnect();
      readyRef.current = false;
      mapRef.current = null;
      map.remove();
    };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !readyRef.current) return;

    syncSources(map, stops, attractions);
  }, [stopsKey, attractionsKey]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !readyRef.current) return;

    fitView(map, stops, center);
  }, [stopsKey, center?.lng, center?.lat]);

  return (
    <div>
      <div
        ref={containerRef}
        style={{
          width: "100%",
          height: "500px",
          minHeight: "500px",
          borderRadius: "12px",
          overflow: "hidden",
        }}
      />
      <div className="flex gap-4 px-3 py-2 text-xs">
        <span className="flex items-center gap-1">
          <span
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#2563eb",
              display: "inline-block",
            }}
          />
          Planned today
        </span>
        <span className="flex items-center gap-1">
          <span
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#ef4444",
              display: "inline-block",
            }}
          />
          Available attractions
        </span>
      </div>
    </div>
  );
}
