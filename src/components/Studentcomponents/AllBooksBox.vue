<template>
  <div style="display: flex; flex-wrap: wrap; justify-content: space-around">
    <div
      v-for="(book, index) in filteredBooks"
      :key="index"
      style="
        width: 30%;
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

      <div style="margin-bottom: 20px">
        <label for="duration">Select Duration:</label>
        <select id="duration" v-model="selectedDuration">
          <option v-for="day in 7" :key="day" :value="day">{{ day }} day(s)</option>
        </select>
      </div>

      <button
        style="
          background-color: green;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
        "
        @click="requestBook(book.id)"
      >
        Request Book
      </button>

      <router-link :to="'/ReadReviews/' + book.id"> Read Reviews</router-link>

    </div>

    <div v-if="showMessage" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 9999; background-color: #000000; color: #ffffff; padding: 20px; border: 2px solid #000000; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);">
      <p>{{ message }}</p>
      <button @click="closeMessage" style="margin-top: 10px; background-color: #ffffff; color: #000000; border: 1px solid #000000; border-radius: 5px; padding: 5px 10px;">Close</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:5000'

export default {
  props: {
    searchQuery: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      books: [],
      selectedDuration: 1, // Default duration selection
      showMessage: false,
      message: ''
    }
  },
  computed: {
    filteredBooks() {
      const query = this.searchQuery.toLowerCase().trim();
      if (query === '') {
        return this.books;
      }
      const filtered = this.books.filter(book => {
        return (
          book.title.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.category.toLowerCase().includes(query)
        );
      });
      console.log('Filtered Books:', filtered);
      return filtered;
    }
  },
  mounted() {
    this.getBookDetails()
  },
  methods: {
    getBookDetails() {
      axios
        .get('/api/get_book_details')
        .then((response) => {
          this.books = response.data
        })
        .catch((error) => {
          console.error('Error fetching book details:', error)
        })
    },
    requestBook(bookId) {
      const token = localStorage.getItem('token') // Get JWT token from localStorage

      axios.post('/api/request_book', {
        book_id: bookId,
        duration: this.selectedDuration
      }, {
        headers: {
          'Authorization': `Bearer ${token}`, // Include token in the request headers
          'Content-Type': 'application/json'
        }
      })
      
      .then(response => {
        console.log(response.data)
        if (response.data.duplicate_request) {
      // Display a message to the user indicating that they have already requested the book
      this.showMessage = true;
      this.message = 'You have already requested this book';
    } else {
          // Display a success message
          this.showMessage = true;
          this.message = 'Book request successful';
        }
      })
      .catch(error => {
        console.error('Error requesting book:', error)
        // Handle error
      })
    },
    
    closeMessage() {
      this.showMessage = false;
    }
  }
}
</script>
