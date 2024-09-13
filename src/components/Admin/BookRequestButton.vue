<template>
  <div class="container">
    <div v-for="request in bookRequests" :key="request.request_id" class="card">
      BOOK Request
      
      <p class="card-text"><strong>Username:</strong> {{ request.username }}</p>
      <p class="card-text"><strong>Book Name:</strong> {{ request.book_title }}</p>
      <p class="card-text"><strong>Status:</strong> {{ request.status }}</p>
      
      <p class="card-text"><strong>Request Date:</strong> {{ request.request_date }}</p>
      <p class="card-text"><strong>Duration:</strong> {{ request.duration }} day(s)</p>
      <div class="button-group">
        <button @click="approveRequest(request.request_id)" class="approve-button">Approve</button>
        <button @click="denyRequest(request.request_id)" class="deny-button">Deny</button>
      </div>
    </div>

    <div v-if="showMessage" class="message">
      <p>{{ message }}</p>
      <button @click="closeMessage" class="close-button">Close</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BookRequest',
  data() {
    return {
      bookRequests: [],
      showMessage: false,
      message: '',
    };
  },
  created() {
    this.fetchBookRequests();
  },
  methods: {
    async fetchBookRequests() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/admin_get_book_request_details');
        this.bookRequests = response.data;
      } catch (error) {
        this.message = 'Error fetching book requests.';
        this.showMessage = true;
      }
    },
    async approveRequest(requestId) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/admin_approve_request', { request_id: requestId });
        if (response.status === 200) {
          this.message = 'Request approved successfully.';
          this.showMessage = true;
          this.fetchBookRequests(); // Refresh the list after approval
        }
      } catch (error) {
        this.message = 'Error approving request.';
        this.showMessage = true;
      }
    },
    async denyRequest(requestId) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/admin_deny_request', { request_id: requestId });
        if (response.status === 200) {
          this.message = 'Request denied successfully.';
          this.showMessage = true;
          this.fetchBookRequests(); // Refresh the list after denial
        }
      } catch (error) {
        this.message = 'Error denying request.';
        this.showMessage = true;
      }
    },
    closeMessage() {
      this.showMessage = false;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20px;
}

.card {
  width: 300px;
  margin: 15px;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: left;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 20px;
  margin-bottom: 10px;
}

.card-text {
  font-size: 14px;
  margin-bottom: 8px;
  color: #333;
}

.card-text strong {
  color: #555;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.approve-button, .deny-button {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.approve-button {
  background-color: #4caf50;
  color: #fff;
}

.approve-button:hover {
  background-color: #45a049;
}

.deny-button {
  background-color: #f44336;
  color: #fff;
}

.deny-button:hover {
  background-color: #e53935;
}

.message {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  background-color: #333;
  color: #fff;
  padding: 20px;
  border: 2px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.close-button {
  margin-top: 10px;
  background-color: #555;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.close-button:hover {
  background-color: #777;
}
</style>
