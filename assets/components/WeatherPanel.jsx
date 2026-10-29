/** Show the forecast matching the currently selected itinerary day. */
export default function WeatherPanel({ destinationName, day, weather, error }) {
  const selected = weather?.find((w) => w.date === day?.date);

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">
        Weather in {destinationName} · Day {day.day_number} ({day.date})
      </h2>

      {error ? (
        <p className="text-sm text-error" role="status">{error}</p>
      ) : selected ? (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <p><span className="font-semibold">Conditions:</span> {selected.conditions}</p>
          <p><span className="font-semibold">High:</span> {selected.tempmax} °C</p>
          <p><span className="font-semibold">Low:</span> {selected.tempmin} °C</p>
          <p><span className="font-semibold">Chance of rain:</span> {selected.precipprob}%</p>
        </div>
      ) : (
        <p className="text-sm opacity-70" role="status">No weather data available for this day.</p>
      )}
    </div>
  );
}