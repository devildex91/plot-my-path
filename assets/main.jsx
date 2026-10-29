import { createRoot } from 'react-dom/client';
import Onboarding from './components/onboarding.jsx';
import SearchBar from './components/searchBar.jsx';
import ItineraryBuilder from './components/itinerary_builder.jsx'

// Mount only the React feature present on the current Django-rendered page.
const rootElement = document.getElementById('onboarding');
const searchRoot = document.getElementById('searchDiv');
const builder = document.getElementById('builder')
 const dataElement = document.getElementById('app-data');


if (rootElement) {
    const homeUrl = rootElement.getAttribute('data-home-url')
    const landingUrl = rootElement.getAttribute('data-landing-url')
   
    createRoot(rootElement).render(
        <Onboarding homeUrl={homeUrl}
          />
    );
}


if (searchRoot) {
    const baseUrl = searchRoot.getAttribute('data-base-url');
    createRoot(searchRoot).render(
    <SearchBar baseUrl={baseUrl} />
    )
}


if (builder) {
    const { trip, preferences, days, attractions, weather, weather_error: weatherError } = JSON.parse(dataElement.textContent);
    createRoot(builder).render(
        <ItineraryBuilder trip={trip} preferences = {preferences} days={days} attractions={attractions} weather={weather} weatherError={weatherError} />
    )
}
