import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

export default function MapView({ aps }) {
  return (
    <MapContainer center={[3.42, -76.53]} zoom={11} style={{ height: 300 }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {aps.map((ap, i) => (
        <Marker key={i} position={[ap.lat, ap.lng]}>
          <Popup>
            {ap.name} - {ap.status}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}