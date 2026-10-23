import React from "react";
import { useState } from "react";

function ItineraryBuilder({ trip, preferences, days, attractions }) {

  const [currentDayIndex, setCurrentDayIndex] = useState(0);
  const [selectedAttractionId, setSelectedAttractionId] = useState("");
const [startTime, setStartTime] = useState("09:00");
const [endTime, setEndTime] = useState("10:00");
const [activityError, setActivityError] = useState("");
 const [daysState, setDaysState] = useState(() =>
  [...(days || [])].sort(
    (a, b) => a.day_number - b.day_number
  )
);

const currentDay = daysState[currentDayIndex];

  const formatDayDate = (dateString) => {
    if (!dateString) return "Date unavailable";

    const [year, month, day] = dateString.split("-").map(Number);
    const date = new Date(year, month - 1, day);

    return new Intl.DateTimeFormat("en-GB", {
      weekday: "short",
      day: "numeric",
      month: "short",
    }).format(date);
  };

  // Handle missing days
  if (!currentDay) {
    return <p>No itinerary days available.</p>;
  }
  

const handleAddActivity = async () => {
  setActivityError("");

  if (!selectedAttractionId) {
    setActivityError("Please choose an attraction.");
    return;
  }

  if (startTime >= endTime) {
    setActivityError("End time must be after start time.");
    return;
  }

  try {
    const response = await fetch(currentDay.add_activity_url, {
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

    // Update the displayed days with the saved activity.
    setDaysState((previousDays) =>
      previousDays.map((day) =>
        day.id === currentDay.id
          ? {
              ...day,
              activities: [...day.activities, result.activity],
            }
          : day
      )
    );

    setSelectedAttractionId("");
    setActivityError("");
  } catch (error) {
    setActivityError(error.message);
  }
};

function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (const cookie of cookies) {
    const [key, ...value] = cookie.trim().split("=");

    if (key === name) {
      return decodeURIComponent(value.join("="));
    }
  }

  return null;
}
  const isFirstDay = currentDayIndex === 0;
  const isLastDay = currentDayIndex === daysState.length - 1;
  return (
    <>
      <div className="tabs tabs-box">
        <input
          type="radio"
          name="my_tabs_6"
          className="tab"
          aria-label="Itinerary"
        />
        <div className="tab-content bg-base-100 border-base-300 p-6">
    {/* Current day title */}
      <div className="flex items-center justify-between">
        <h3 className="font-extrabold text-sm text-base-content tracking-tight">
          Day {currentDay.day_number} –{" "}
          {formatDayDate(currentDay.date)}
        </h3>

        <span className="text-sm">
          Day {currentDayIndex + 1} of {daysState.length}
        </span>
      </div>
      
<div className="space-y-3 rounded-lg border p-4">
  <h4 className="font-bold">Add an activity</h4>

  <select
    className="select select-bordered w-full"
    value={selectedAttractionId}
    onChange={(e) => setSelectedAttractionId(e.target.value)}
  >
    <option value="">Choose an attraction...</option>

    {attractions.map((attraction) => (
      <option key={attraction.id} value={attraction.id}>
        {attraction.name}
      </option>
    ))}
  </select>

  <div className="grid grid-cols-2 gap-3">
    <label className="form-control">
      <span className="label-text">Start time</span>
      <input
        type="time"
        className="input input-bordered"
        value={startTime}
        onChange={(e) => setStartTime(e.target.value)}
      />
    </label>

    <label className="form-control">
      <span className="label-text">End time</span>
      <input
        type="time"
        className="input input-bordered"
        value={endTime}
        onChange={(e) => setEndTime(e.target.value)}
      />
    </label>
  </div>

  {activityError && (
    <p className="text-sm text-error">{activityError}</p>
  )}

  <button
    type="button"
    className="btn btn-primary w-full"
    onClick={handleAddActivity}
  >
    Add activity
  </button>
</div>

      {/* Activities for the selected day */}
      <div className="space-y-4">
        {currentDay.activities?.length > 0 ? (
          currentDay.activities.map((activity) => {
            const attraction = attractions.find(
              (item) => item.id === activity.attraction_id
            );

            return (
              <div
                key={activity.id}
                className="rounded-lg border p-4"
              >
                <h4 className="font-bold">
                  {attraction?.name || "Unknown attraction"}
                </h4>

                <p className="text-sm">
                  {activity.start_time.slice(0, 5)} –{" "}
                  {activity.end_time.slice(0, 5)}
                </p>

                {attraction?.description && (
                  <p className="text-sm mt-2">
                    {attraction.description}
                  </p>
                )}

                {activity.notes && (
                  <p className="text-sm mt-2">
                    {activity.notes}
                  </p>
                )}
              </div>
            );
          })
        ) : (
          <p className="text-sm text-base-content/70">
            No activities planned for this day yet.
          </p>
        )}
      </div>

      {/* Navigation between days */}
      <div className="flex items-center justify-between gap-4">
        <button
          type="button"
          className="btn btn-outline"
          disabled={isFirstDay}
          onClick={() =>
            setCurrentDayIndex((index) => index - 1)
          }
        >
          ❮
        </button>

        <button
          type="button"
          className="btn btn-primary"
          disabled={isLastDay}
          onClick={() =>
            setCurrentDayIndex((index) => index + 1)
          }
        >
         ❯
        </button>
        
      </div>

        </div>

        <input
          type="radio"
          name="my_tabs_6"
          className="tab"
          aria-label="Map"
          defaultChecked
        />
        <div className="tab-content bg-base-100 border-base-300 p-6">
          Tab content 2
        </div>

        <input
          type="radio"
          name="my_tabs_6"
          className="tab"
          aria-label="Weather"
        />
        <div className="tab-content bg-base-100 border-base-300 p-6">
          Tab content 3
        </div>
      </div>
    </>
  );
}

export default ItineraryBuilder;
