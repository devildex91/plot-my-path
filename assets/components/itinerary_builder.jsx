import React, { useState } from "react";
import ItineraryMap from "./ItineraryMap";
import ActivityList from "./ActivityList";
import AddActivityForm from "./AddActivityForm";
import WeatherPanel from "./WeatherPanel";
import { getCookie } from "./utils";

const isValidCoord = (lat, lng) => Number.isFinite(lat) && Number.isFinite(lng);

/** Render and manage the interactive itinerary for the selected trip day. */
function ItineraryBuilder({
  trip,
  preferences,
  days,
  attractions,
  weather,
  weatherError,
}) {
  const [currentDayIndex, setCurrentDayIndex] = useState(0);
  const [deletingActivityId, setDeletingActivityId] = useState(null);
  const [deleteError, setDeleteError] = useState("");

  const [daysState, setDaysState] = useState(() => {
    const tripDays = Array.isArray(trip?.trip_days)
      ? trip.trip_days
      : Array.isArray(days)
        ? days
        : [];

    return [...tripDays].sort((a, b) => a.day_number - b.day_number);
  });

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

  if (!currentDay) {
    return <p>No itinerary days available.</p>;
  }

  const updateCurrentDayActivities = (updater) => {
    setDaysState((previousDays) =>
      previousDays.map((day) =>
        day.id === currentDay.id
          ? { ...day, activities: updater(day.activities || []) }
          : day,
      ),
    );
  };

  const handleActivityAdded = (activity) => {
    updateCurrentDayActivities((existing) => [...existing, activity]);
  };

  const handleRemoveActivity = async (activityId) => {
    setDeleteError("");
    setDeletingActivityId(activityId);

    const deleteUrl = `/trips/${trip.id}/itinerary/activities/${activityId}/delete/`;

    try {
      const response = await fetch(deleteUrl, {
        method: "DELETE",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
      });

      if (!response.ok) {
        const result = await response.json().catch(() => ({}));
        throw new Error(
          result.error || "Could not remove this activity from the server.",
        );
      }

      updateCurrentDayActivities((existing) =>
        existing.filter((act) => act.id !== activityId),
      );
    } catch (error) {
      setDeleteError(error.message || "Could not delete activity.");
    } finally {
      setDeletingActivityId(null);
    }
  };

  const isFirstDay = currentDayIndex === 0;
  const isLastDay = currentDayIndex === daysState.length - 1;
  const activities = currentDay.activities || [];

  // Split the overall trip budget evenly across days for a simple daily estimate.
  const dailyBudget = trip.budget / daysState.length;
  const totalDailySpent = activities.reduce((sum, activity) => {
    const attraction = attractions.find(
      (item) => String(item.id) === String(activity.attraction_id),
    );
    return sum + (Number(attraction?.entry_cost) || 0);
  }, 0);
  const dailyRemaining = dailyBudget - totalDailySpent;

  const lat = parseFloat(trip?.destination?.latitude);
  const lng = parseFloat(trip?.destination?.longitude);
  const position = isValidCoord(lat, lng) ? { lat, lng } : null;

  const activityPositions = activities
    .map((activity) => {
      const attraction = attractions.find(
        (item) => String(item.id) === String(activity.attraction_id),
      );
      const aLat = parseFloat(attraction?.latitude);
      const aLng = parseFloat(attraction?.longitude);

      return isValidCoord(aLat, aLng)
        ? {
            id: activity.id,
            attractionId: attraction.id, // new
            lat: aLat,
            lng: aLng,
            name: attraction?.name,
          }
        : null;
    })
    .filter(Boolean);

  const attractionPositions = attractions
    .map((a) => {
      const aLat = parseFloat(a.latitude);
      const aLng = parseFloat(a.longitude);
      return isValidCoord(aLat, aLng)
        ? { id: a.id, lat: aLat, lng: aLng, name: a.name }
        : null;
    })
    .filter(Boolean);

  return (
    <div className="tabs tabs-box">
      <input
        type="radio"
        name="my_tabs_6"
        className="tab"
        aria-label="Itinerary"
      />
      <div className="tab-content bg-base-100 border-base-300 p-6">
        <div className="space-y-6">
          <header className="space-y-1">
            <h2 className="text-2xl font-bold">
              Day {currentDay.day_number ?? currentDayIndex + 1}
            </h2>
            <p className="text-sm text-base-content/70">
              {formatDayDate(currentDay.date)}
            </p>
            <p>Today's budget: £{dailyBudget.toFixed(2)}</p>
            <p>Remaining budget: £{dailyRemaining.toFixed(2)}</p>
          </header>

          <ActivityList
            activities={activities}
            attractions={attractions}
            onRemove={handleRemoveActivity}
            deletingActivityId={deletingActivityId}
            error={deleteError}
          />

          <nav
            className="flex items-center justify-between gap-4"
            aria-label="Itinerary days"
          >
            <button
              type="button"
              className="btn btn-outline"
              disabled={isFirstDay}
              onClick={() => setCurrentDayIndex((index) => index - 1)}
              aria-label="Previous day"
            >
              Previous day
            </button>

            <span className="text-sm">
              Day {currentDayIndex + 1} of {daysState.length}
            </span>

            <button
              type="button"
              className="btn btn-primary"
              disabled={isLastDay}
              onClick={() => setCurrentDayIndex((index) => index + 1)}
              aria-label="Next day"
            >
              Next day
            </button>
          </nav>

          <AddActivityForm
            key={currentDay.id}
            attractions={attractions}
            activities={activities}
            addUrl={currentDay.add_activity_url}
            onAdded={handleActivityAdded}
          />
        </div>
      </div>

      <input
        type="radio"
        name="my_tabs_6"
        className="tab"
        aria-label="Maps"
        defaultChecked
      />
      <div className="tab-content bg-base-100 border-base-300 p-0 overflow-hidden">
        <ItineraryMap
          center={position}
          stops={activityPositions}
          attractions={attractionPositions}
        />
      </div>

      <input
        type="radio"
        name="my_tabs_6"
        className="tab"
        aria-label="Weather"
      />
      <div className="tab-content bg-base-100 border-base-300 p-6">
        <WeatherPanel
          destinationName={trip?.destination?.name}
          day={currentDay}
          weather={weather}
          error={weatherError}
        />
      </div>
    </div>
  );
}

export default ItineraryBuilder;
