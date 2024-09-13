<template>
  Approved Books
  <div style="display: flex; flex-wrap: wrap; justify-content: space-around">
    <div
      v-for="(book, index) in approvedBooks"
      :key="index"
      style="
        width: 30%;
        height: 300px;
        margin-bottom: 20px;
        background-color: rgba(255, 255, 255, 0.15);
        border: 1px solid #000;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
      "
    >
    
      <h2 style="font-size: 24px">{{ book.title }}</h2>
      <p
        style="
          font-size: 16px;
          text-align: left;
          margin-top: 20px;
          color: aliceblue;
          margin-bottom: 20px;
        "
      >
        Author: {{ book.author }}
      </p>
      <p style="font-size: 14px; text-align: left; color: aliceblue; margin-bottom: 20px">
        Category: {{ book.category }}
      </p>

      <p style="font-size: 12px; text-align: left; color: aliceblue; margin-bottom: 20px">
        Issue Date: {{ book.issue_date }}
      </p>

      <p style="font-size: 12px; text-align: left; color: aliceblue; margin-bottom: 20px">
        Due Date: {{ book.return_date }}
      </p>
      <button
        style="
          background-color: green;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
        "
        @click="navigateToViewBook(book.book_id)"
      >
        Read Book
      </button>

      <router-link :to="'/ReadReviews/' + book.book_id"> Read Reviews</router-link>

      <button class="btn btn-danger" @click="deleteBookRequest(book.request_id)">Return </button>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:5000'

// Adding request interceptor to include the token in headers
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  data() {
    return {
      approvedBooks: []
    }
  },
  mounted() {
    this.getApprovedBooks()
  },
  methods: {
    getApprovedBooks() {
      axios
        .get('/api/get_approved_books') // Fetch only approved books
        .then((response) => {
          this.approvedBooks = response.data // Assign approved books to the approvedBooks array
        })
        .catch((error) => {
          console.error('Error fetching approved books:', error)
        })
    },
    readBook(bookId) {
      this.$router.push({ name: 'view-book', params: { bookId: bookId }});
    },
    deleteBookRequest(requestId) {
      axios
        .post('/api/delete_book_request', { request_id: requestId })
        .then((response) => {
          console.log('Book request deleted successfully')
          // Optionally, update the UI to reflect the deletion
          this.getApprovedBooks(); // Refresh the list of approved books
        })
        .catch((error) => {
          console.error('Error deleting book request:', error)
        })
    },
    navigateToViewBook(bookId) {
      // Push the route with the bookId parameter to the named route 'view-book'
      this.$router.push({ name: 'view-book', params: { bookId: bookId }});
    }
  }
}
</script>
