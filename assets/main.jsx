import { createRoot } from "react-dom/client";
import Onboarding from "./components/onboarding.jsx";
import SearchBar from "./components/searchBar.jsx";
import ItineraryBuilder from "./components/itinerary_builder.jsx";

// Mount only the React feature present on the current Django-rendered page.
const rootElement = document.getElementById("onboarding");
const searchRoot = document.getElementById("searchDiv");
const builder = document.getElementById("builder");
const dataElement = document.getElementById("app-data");

if (rootElement) {
  const homeUrl = rootElement.getAttribute("data-home-url");
  const landingUrl = rootElement.getAttribute("data-landing-url");

  createRoot(rootElement).render(<Onboarding homeUrl={homeUrl} />);
}

if (searchRoot) {
  const baseUrl = searchRoot.getAttribute("data-base-url");
  createRoot(searchRoot).render(<SearchBar baseUrl={baseUrl} />);
}

if (builder) {
  const {
    trip,
    preferences,
    days,
    attractions,
    weather,
    weather_error: weatherError,
  } = JSON.parse(dataElement.textContent);
  createRoot(builder).render(
    <ItineraryBuilder
      trip={trip}
      preferences={preferences}
      days={days}
      attractions={attractions}
      weather={weather}
      weatherError={weatherError}
    />,
  );
}

// Standard js code for django templates not using react
// Theme toggle
const toggle = document.getElementById("theme-toggle");
const root = document.documentElement;

if (toggle) {
  toggle.checked = root.getAttribute("data-theme") === "sunset";

  toggle.addEventListener("change", () => {
    const theme = toggle.checked ? "sunset" : "fantasy";
    root.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  });
}

// Payment flow event handler
document.addEventListener("click", async (e) => {
  const btn = e.target.closest("#checkout-button");
  if (!btn || btn.disabled) return;

  btn.disabled = true;

  try {
    const res = await fetch(btn.dataset.url, {
      method: "POST",
      headers: { "X-CSRFToken": btn.dataset.csrf },
    });
    const data = await res.json();

    if (data.checkout_url) {
      window.location.href = data.checkout_url;
      return;
    }
    alert(data.error || "Error: Unable to proceed to payment");
  } catch (err) {
    alert("Payment processing failed");
  }
  btn.disabled = false;
});
// Favourite button for Django-rendered destination cards
document.addEventListener("click", async (e) => {
  const button = e.target.closest(".favourite-btn");

  if (!button || button.disabled) return;

  button.disabled = true;

  try {
    const response = await fetch(button.dataset.url, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not update favourite.");
    }

    const icon = button.querySelector("i");

    if (data.is_favourite) {
      icon.classList.replace("fa-regular", "fa-solid");
      icon.classList.add("text-red-500");
      button.setAttribute("aria-label", "Remove from favourites");
    } else {
      icon.classList.replace("fa-solid", "fa-regular");
      icon.classList.remove("text-red-500");
      button.setAttribute("aria-label", "Add to favourites");
    }

  } catch (error) {
    console.error("Favourite error:", error);
  } finally {
    button.disabled = false;
  }
});

// Retrieve Django CSRF cookie
function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (const cookie of cookies) {
    const cookieValue = cookie.trim();

    if (cookieValue.startsWith(name + "=")) {
      return decodeURIComponent(
        cookieValue.substring(name.length + 1)
      );
    }
  }

  return null;
}