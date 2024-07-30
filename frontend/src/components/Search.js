import React, { useState } from 'react';
import axios from 'axios';
import './Search.css';

const Search = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = (e) => {
        e.preventDefault();
        axios.get(`http://127.0.0.1:8000/api/traders/?search=${searchTerm}`)
            .then(response => {
                setResults(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the search results!', error);
            });
    };

    return (
        <div className="search-container">
            <h2>Search Traders</h2>
            <form onSubmit={handleSearch}>
                <div className="form-group">
                    <input
                        type="text"
                        placeholder="Search by name or service"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <button type="submit">Search</button>
                </div>
            </form>
            <div className="search-results">
                {results.map(result => (
                    <div key={result.trader_id} className="search-result">
                        <h3>{result.name}</h3>
                        <p>{result.services}</p>
                        <p>{result.location}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Search;
