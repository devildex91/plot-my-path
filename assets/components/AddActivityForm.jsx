import { useState } from "react";
import { formatActivityTime, getCookie } from "./utils";

/** Validate and submit a new attraction activity for the currently selected day. */
export default function AddActivityForm({
  attractions,
  activities,
  addUrl,
  onAdded,
}) {
  const [selectedAttractionId, setSelectedAttractionId] = useState("");
  const [startTime, setStartTime] = useState("09:00");
  const [endTime, setEndTime] = useState("10:00");
  const [error, setError] = useState("");
  const [isAdding, setIsAdding] = useState(false);

  const handleAdd = async () => {
    setError("");

    if (!selectedAttractionId) {
      setError("Please choose an attraction.");
      return;
    }

    if (startTime >= endTime) {
      setError("End time must be after start time.");
      return;
    }

    const newStart = formatActivityTime(startTime);
    const newEnd = formatActivityTime(endTime);

    // Reject overlapping intervals before sending the request to the server.
    const hasConflict = activities.some((activity) => {
      const existingStart = formatActivityTime(activity.start_time);
      const existingEnd = formatActivityTime(activity.end_time);

      return newStart < existingEnd && newEnd > existingStart;
    });

    if (hasConflict) {
      setError("This time slot overlaps with an already scheduled activity.");
      return;
    }

    setIsAdding(true);

    try {
      const response = await fetch(addUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          attraction_id: Number(selectedAttractionId),
          start_time: startTime,
          end_time: endTime,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Could not add activity.");
      }

      if (!result.activity) {
        throw new Error("The server did not return the new activity.");
      }

      onAdded(result.activity);
      setSelectedAttractionId("");
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <div className="collapse bg-base-100 border border-base-300">
      <input type="checkbox" />
      <div className="collapse-title font-semibold">+ Add Activity</div>
      <div className="collapse-content text-sm">
        <section className="space-y-4 rounded-lg border p-4">
          <h3 className="text-lg font-bold">Add an activity</h3>

          <label className="form-control w-full">
            <span className="label-text mb-2">Attraction</span>
            <select
              className="select select-bordered w-full"
              value={selectedAttractionId}
              onChange={(event) => setSelectedAttractionId(event.target.value)}
              disabled={isAdding}
            >
              <option value="">Choose an attraction</option>
              {attractions.map((attraction) => (
                <option key={attraction.id} value={attraction.id}>
                  {attraction.name}
                </option>
              ))}
            </select>
          </label>

          <div className="grid grid-cols-2 gap-3">
            <label className="form-control">
              <span className="label-text mb-2">Start time</span>
              <input
                type="time"
                className="input input-bordered w-full"
                value={startTime}
                onChange={(event) => setStartTime(event.target.value)}
                disabled={isAdding}
                required
              />
            </label>

            <label className="form-control">
              <span className="label-text mb-2">End time</span>
              <input
                type="time"
                className="input input-bordered w-full"
                value={endTime}
                onChange={(event) => setEndTime(event.target.value)}
                disabled={isAdding}
                required
              />
            </label>
          </div>

          {error && (
            <p className="text-sm text-error" role="alert">
              {error}
            </p>
          )}

          <button
            type="button"
            className="btn btn-primary w-full"
            onClick={handleAdd}
            disabled={isAdding}
          >
            {isAdding ? "Adding..." : "Add activity"}
          </button>
        </section>
      </div>
    </div>
  );
}
