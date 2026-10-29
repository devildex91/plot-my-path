/** Read a named cookie, preserving any equals signs in its value. */
export function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (const cookie of cookies) {
    const [key, ...value] = cookie.trim().split("=");

    if (key === name) {
      return decodeURIComponent(value.join("="));
    }
  }

  return null;
}

/** Normalize either a time or ISO datetime string to an HH:MM value. */
export function formatActivityTime(isoString) {
  if (!isoString) return "00:00";

  if (isoString.includes("T")) {
    return isoString.split("T")[1]?.slice(0, 5) || "00:00";
  }

  return isoString.slice(0, 5);
}