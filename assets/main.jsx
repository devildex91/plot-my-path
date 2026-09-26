import { createRoot } from 'react-dom/client';

const rootElement = document.getElementById('root');

if (rootElement) {
    createRoot(rootElement).render(
        <h1 className="text-3xl font-bold text-primary">
            Plot My Path
        </h1>
    );
}