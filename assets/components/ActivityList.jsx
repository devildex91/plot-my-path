import { formatActivityTime } from "./utils";

/** Display the selected day's activities and expose their removal action. */
export default function ActivityList({
  activities,
  attractions,
  onRemove,
  deletingActivityId,
  error,
}) {
  return (
    <section className="space-y-4" aria-label="Planned activities">
      <ul className="list bg-base-100 rounded-box shadow-md">
        <li className="p-4 pb-2 text-xs opacity-60 tracking-wide">
          Planned Activities
        </li>

        {activities.length ? (
          activities.map((activity) => {
            const attraction = attractions.find(
              (item) => String(item.id) === String(activity.attraction_id),
            );
            const isDeleting = deletingActivityId === activity.id;

            return (
              <li key={activity.id} className="list-row p-2">
                <div>
                  <img
                    className="size-10 rounded-box"
                    src={attraction?.image_url}
                    alt={attraction?.name}
                  />
                </div>
                <div>
                  <div>{attraction?.name || "Unknown attraction"}</div>
                  <div className="text-xs uppercase font-semibold opacity-60">
                    {formatActivityTime(activity.start_time)} -{" "}
                    {formatActivityTime(activity.end_time)}
                    <p>£{attraction?.entry_cost}pp</p>
                  </div>
                </div>
                <p className="list-col-wrap text-xs">
                  {attraction?.description}
                </p>
                <button
                  type="button"
                  className={`btn btn-sm btn-error btn-outline ${isDeleting ? "loading" : ""}`}
                  onClick={() => onRemove(activity.id)}
                  disabled={deletingActivityId !== null}
                >
                  {isDeleting ? "" : "Remove"}
                </button>
              </li>
            );
          })
        ) : (
          <li className="p-4 text-sm text-base-content/70">
            No activities planned for this day yet.
          </li>
        )}
      </ul>

      {error && (
        <p className="text-sm text-error" role="alert">
          {error}
        </p>
      )}
    </section>
  );
}
