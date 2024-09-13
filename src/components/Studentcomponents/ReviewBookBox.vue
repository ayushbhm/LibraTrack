<template>
  <div>
    <textarea
      v-model="review"
      class="dark-textarea"
      placeholder="Enter your review..."
    ></textarea>
    <button @click="postReview" class="btn btn-success" style="margin-top: 10px;">Post Review</button>
  </div>
</template>

<script>
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:5000'; // Set your Flask API base URL here

export default {
  props: ['bookId'], // Define the bookId prop to receive the book ID from the parent component
  data() {
    return {
      review: ''
    };
  },
  methods: {
    postReview() {
      if (this.review === '') {
        alert('Please provide a review before posting.');
        return;
      }

      const data = {
        book_id: this.bookId, // Use the received bookId prop
        review: this.review
      };

      const token = localStorage.getItem('token'); // Get the JWT token from local storage

      axios.post('/api/post_review', data, {
        headers: {
          Authorization: `Bearer ${token}` // Include the token in the request headers
        }
      })
      .then(response => {
        console.log('Review posted successfully:', response.data.message);
        // Optionally, you can perform any additional actions after posting the review
        this.review = ''; // Clear the review text after posting the review
      })
      .catch(error => {
        console.error('Error posting review:', error);
      });
    }
  }
};
</script>

<style scoped>
.dark-textarea {
  width: 600px;
  height: 100px;
  background-color: #333; /* Dark background */
  color: #fff; /* White text */
  border: 2px solid #fff; /* White border */
  padding: 10px;
}

/* Removed rating-section and dark-select styles */
.dark-button {
  background-color: #333; /* Dark background */
  color: #fff; /* White text */
  border: 2px solid #fff; /* White border */
  padding: 5px 10px;
  cursor: pointer;
}
</style>
