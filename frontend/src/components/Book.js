import React, { useState } from 'react';
import axios from 'axios';
import './Book.css';

const Book = () => {
    const [formData, setFormData] = useState({
        user_id: '',
        trader_id: '',
        service: '',
        appointment_time: '',
    });

    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://127.0.0.1:8000/api/appointments/', formData)
            .then(response => {
                setSuccessMessage('Appointment booked successfully!');
                setErrorMessage('');
            })
            .catch(error => {
                setErrorMessage('Failed to book appointment.');
                setSuccessMessage('');
            });
    };

    return (
        <div className="book-container">
            <h2>Book Appointment</h2>
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
                    <label>Service</label>
                    <input
                        type="text"
                        name="service"
                        placeholder="Service"
                        value={formData.service}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label>Appointment Time</label>
                    <input
                        type="datetime-local"
                        name="appointment_time"
                        value={formData.appointment_time}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit">Book</button>
            </form>
        </div>
    );
};

export default Book;
