<template>
    
      <button @click="toggleUserProfile" class="profile-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
          </svg>
      </button>
  <div>
      <!-- User Profile Popup -->
      <div v-if="showUserProfile" class="user-profile">
        <h3>My Profile</h3>
        <p><strong>Username:</strong> {{ userProfile.username }}</p>
        <p><strong>Email:</strong> {{ userProfile.email }}</p>
        <p><strong>Approved Books:</strong> {{ userProfile.num_approved_books }}</p>
        <p><strong>Pending Book Requests:</strong> {{ userProfile.num_pending_requests }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  axios.defaults.baseURL = 'http://127.0.0.1:5000';
  
  export default {
    data() {
      return {
        showUserProfile: false,
        userProfile: {}
      };
    },
    methods: {
      toggleUserProfile() {
        this.showUserProfile = !this.showUserProfile;
        if (this.showUserProfile) {
          this.fetchUserProfile();
        }
      },
      async fetchUserProfile() {
        try {
          const response = await axios.get('/api/user_profile');
          this.userProfile = response.data;
        } catch (error) {
          console.error('Error fetching user profile:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
 
  
  .user-profile {
    position: absolute;
    top: 80px; /* Adjust as needed */
    left: 50%; /* Center horizontally */
    transform: translateX(-50%);
    background-color: #515151; /* Dark grey background */
    color: #fff; /* White text */
    border: 1px solid #ccc;
    padding: 40px; /* Increased padding for a larger box */
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2); /* Increased shadow */
  }
  </style>
  