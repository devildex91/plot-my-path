import { createRoot } from 'react-dom/client';
import Onboarding from './components/onboarding.jsx';
import SearchBar from './components/searchBar.jsx';
const rootElement = document.getElementById('onboarding');
const searchRoot = document.getElementById('searchDiv');
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