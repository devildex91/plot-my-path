import React, {useState, useEffect } from "react";

function SearchBar({ onSearch}) {
const [query, setQuery] = useState('');
const [results, setResults] = useState([]);
const [isLoading, setIsLoading]= useState(false);

 useEffect(() => {
 
    if (!query.trim()) {
      setResults([]);
      return;
    }

   
    const delayDebounceFn = setTimeout(async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`/destination/api/search/?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        setResults(data.results);
      } catch (error) {
        console.error("Search failed:", error);
      } finally {
        setIsLoading(false);
      }
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  return (
    <div className="search-container">
      <label className="input">
  <svg className="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g
      strokeLinejoin="round"
      strokeLinecap="round"
      strokeWidth="2.5"
      fill="none"
      stroke="currentColor"
    >
      <circle cx="11" cy="11" r="8"></circle>
      <path d="m21 21-4.3-4.3"></path>
    </g>
  </svg>
  <input type="text" 
  className="grow" 
  placeholder="Search Destinations..."
  value={query}
   onChange={(e) => setQuery(e.target.value)} />

</label>
      {isLoading && <div className="spinner">Loading...</div>}

      {results.length > 0 && (
        <ul className="results-dropdown">
          {results.map((item) => (
  <li key={item.id} className="search-result-item">
    
    <a href={`/destinations/${item.id}/`} className="search-result-link">
      
      
      <img 
        src={item.image_url} 
        alt={item.name} 
        className="w-20 h-auto" 
      />
      
      <div className="search-result-text">
        <span className="destination-name">{item.name}</span>
        <span className="destination-country">{item.country}</span>
      </div>

    </a>
  </li>
))}

        </ul>
      )}
    </div>
  );
}
export default SearchBar;