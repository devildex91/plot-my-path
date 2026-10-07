import { createRoot } from 'react-dom/client';
import Onboarding from './components/onboarding.jsx';
const rootElement = document.getElementById('onboarding');

if (rootElement) {
    const homeUrl = rootElement.getAttribute('data-home-url')
    const landingUrl = rootElement.getAttribute('data-landing-url')
    createRoot(rootElement).render(
        <Onboarding homeUrl={homeUrl}
          />
    );
}