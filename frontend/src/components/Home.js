import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
    return (
        <div className="home-container">
            <h1>Welcome to Our Service Platform</h1>
            <div className="home-links">
                <Link to="/register">Register</Link>
                <Link to="/login">Login</Link>
                <Link to="/search">Search</Link>
            </div>
        </div>
    );
};

export default Home;
