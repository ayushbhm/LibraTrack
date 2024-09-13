<template>
    Rejected Books
    <div
      v-for="(book, index) in books"
      :key="index"
      style="display: flex; flex-wrap: wrap; justify-content: space-around"
    >
      <div
        v-if="book.status === 'rejected'"
        style="
          width: 30%;
          height: 250px;
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
            Request Date: {{ book.request_date }}
          </p>
  
        <button class="btn btn-danger" @click="deleteBookRequest(book.request_id)">Delete Request</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  axios.defaults.baseURL = 'http://127.0.0.1:5000'
  
  export default {
    data() {
      return {
        books: []
      }
    },
    mounted() {
      this.getBookDetails()
    },
    methods: {
      getBookDetails() {
        axios
          .get('/api/get_book_requests') // Modify the API URL to match the endpoint
          .then((response) => {
            this.books = response.data // Assign all fetched books to the books array
          })
          .catch((error) => {
            console.error('Error fetching book details:', error)
          })
      },
      deleteBookRequest(requestId) {
        axios
          .post('/api/delete_book_request', { request_id: requestId })
          .then((response) => {
            console.log('Book request deleted successfully')
            // Optionally, update the UI to reflect the deletion
            // For example, remove the deleted book from the books array
            this.books = this.books.filter((book) => book.request_id !== requestId)
          })
          .catch((error) => {
            console.error('Error deleting book request:', error)
          })
      }
    }
  }
  </script>
  