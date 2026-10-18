import React, {useState, useEffect } from "react";

function SearchBar({ onSearch, baseUrl }) {
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
    
    <div className="search-container input-primary">
      <label className="input text-primary">
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
  className="grow text-primary relative" 
  placeholder="Search Destinations..."
  value={query}
   onChange={(e) => setQuery(e.target.value)} />

</label>
      {isLoading && <div className="spinner">Loading...</div>}

      {results.length > 0 && (
        <ul className="results-dropdown absolute z-999 bg-base-200 p-2 border border-primary rounded-xl text-primary ">
          {results.map((item) => { 
           const dynamicUrl = baseUrl ? baseUrl.replace('0', item.id) : `/destinations/details/${item.id}/`;
 
            return (
  <li key={item.id} className="search-result-item border border-primary rounded-xl m-2">
    
    <a href={dynamicUrl} className="search-result-link">
      
      
      <img 
        src={item.image_url} 
        alt={item.name} 
        className="w-20 h-auto rounded-t-xl" 
      />
      
      <div className="search-result-text text-center">
        <span className="destination-name">{item.name}</span>
        <span className="destination-country">{item.country}</span>
      </div>

    </a>
  </li>
)})}

        </ul>
      )}
    </div>
  );
}
export default SearchBar;