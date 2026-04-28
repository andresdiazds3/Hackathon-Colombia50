import L from "leaflet";

const createIcon = (color) =>
  new L.Icon({
    iconUrl: `https://maps.google.com/mapfiles/ms/icons/${color}-dot.png`,
    iconSize: [32, 32]
  });

export const greenIcon = createIcon("green");
export const redIcon = createIcon("red");
export const yellowIcon = createIcon("yellow");