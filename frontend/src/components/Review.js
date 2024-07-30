import React, { useState } from 'react';
import axios from 'axios';
import './Review.css';

const Review = () => {
    const [formData, setFormData] = useState({
        user_id: '',
        trader_id: '',
        rating: '',
        comment: ''
    });

    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://127.0.0.1:8000/api/reviews/', formData)
            .then(response => {
                setSuccessMessage('Review submitted successfully!');
                setErrorMessage('');
            })
            .catch(error => {
                setErrorMessage('Failed to submit review.');
                setSuccessMessage('');
            });
    };

    return (
        <div className="review-container">
            <h2>Submit Review</h2>
            {successMessage && <p className="success">{successMessage}</p>}
            {errorMessage && <p className="error">{errorMessage}</p>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>User ID</label>
                    <input
                        type="text"
                        name="user_id"
                        placeholder="User ID"
                        value={formData.user_id}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label>Trader ID</label>
                    <input
                        type="text"
                        name="trader_id"
                        placeholder="Trader ID"
                        value={formData.trader_id}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label>Rating</label>
                    <input
                        type="number"
                        name="rating"
                        placeholder="Rating"
                        value={formData.rating}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label>Comment</label>
                    <textarea
                        name="comment"
                        placeholder="Comment"
                        value={formData.comment}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default Review;
