import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Profile.css';

const Profile = () => {
    const [profileData, setProfileData] = useState({});

    useEffect(() => {
        // Replace '1' with dynamic user ID
        axios.get('http://127.0.0.1:8000/api/users/1/')
            .then(response => {
                setProfileData(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the profile data!', error);
            });
    }, []);

    return (
        <div className="profile-container">
            <h2>Profile</h2>
            <div className="profile-details">
                <p><strong>Name:</strong> {profileData.name}</p>
                <p><strong>Email:</strong> {profileData.email}</p>
                <p><strong>Role:</strong> {profileData.role}</p>
                <p><strong>Membership:</strong> {profileData.membership}</p>
                <p><strong>Location:</strong> {profileData.location}</p>
            </div>
        </div>
    );
};

export default Profile;
