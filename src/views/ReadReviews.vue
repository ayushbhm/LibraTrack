<template>
  <div>
    <StudentNavbar />

    <div class="container">
      <h2 class="text-center mb-4">Book Reviews</h2>

      <!-- Display book information -->
      <div v-if="reviews.length > 0">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title text-white">Book: {{ reviews[0].title }}</h5>
            <p class="card-text text-white">Author: {{ reviews[0].author }}</p>
            <p class="card-text text-white">Category: {{ reviews[0].category }}</p>
          </div>
        </div>
      </div>

      <!-- Display reviews list -->
      <div v-if="reviews.length === 0" class="alert">
        No reviews available for this book.
      </div>
      <div v-else>
        <ul class="list-group">
          <li v-for="(review, index) in reviews" :key="index" class="list-group-item">
            <p class="text-white">"{{ review.review }}" - <span class="text-white">{{ review.username }}</span></p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import StudentNavbar from '../components/Studentcomponents/Studentnavbar.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

axios.defaults.baseURL = 'http://127.0.0.1:5000';

const reviews = ref([]);
const route = useRoute();

onMounted(async () => {
  try {
    const response = await axios.get(`/readreviews/${route.params.bookId}`);
    reviews.value = response.data;
  } catch (error) {
    console.error('Error fetching reviews:', error);
  }
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #333; /* Grey background */
}

.card {
  margin-bottom: 20px;
  background-color: #444; /* Darker grey card background */
  border: 1px solid #555; /* Dark border */
}

.alert {
  margin-top: 20px;
  background-color: #555; /* Darker grey alert background */
  border: 1px solid #666; /* Dark border */
}

.list-group-item {
  margin-bottom: 10px;
  background-color: #444; /* Darker grey list item background */
  border: 1px solid #555; /* Dark border */
  text-emphasis-color: #fff;
}
</style>
