<template>
    <div>
      <!-- Display approved books -->
      <div v-for="book in books" :key="book.id" class="book-box">
        <div class="book-details">
          <h3 class="book-title">{{ book.title }}</h3>
          <h4 class="book-author">{{ book.author }}</h4>
          <h5 class="book-category">{{ book.category }}</h5>
        </div>
        <button @click="fetchAllocations(book.id)" class="view-button">View Allocations</button>
      </div>
  
      <!-- Popup for Allocations -->
      <div v-if="showPopup" class="popup">
        <div class="popup-content">
          <span class="close" @click="closePopup">&times;</span>
          <h2 class="popup-title">Allocations for {{ currentBookTitle }}</h2>
          <ul>
            <li v-for="req in allocations" :key="req.request_id" class="allocation-item">
              <p class="allocation-info">Username: <strong>{{ req.username }}</strong></p>
              <p class="allocation-info">Status: <strong>{{ req.status }}</strong></p>
              <button @click="revokeAccess(req.request_id)" class="revoke-button">Revoke Access</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        books: [], // List of approved books
        allocations: [], // Allocations for the selected book
        showPopup: false, // Toggle popup visibility
        currentBookTitle: '', // Title of the book whose allocations are displayed
        currentBookId: null // ID of the book whose allocations are displayed
      };
    },
    methods: {
      fetchBooks() {
        fetch('http://127.0.0.1:5000/approved_books')
          .then(response => response.json())
          .then(data => {
            this.books = data;
          })
          .catch(error => {
            console.error('Error fetching books:', error);
          });
      },
      fetchAllocations(bookId) {
        fetch(`http://127.0.0.1:5000/alloted_books/${bookId}`)
          .then(response => response.json())
          .then(data => {
            this.allocations = data;
            this.currentBookId = bookId;
            this.currentBookTitle = this.books.find(book => book.id === bookId).title;
            this.showPopup = true;
          })
          .catch(error => {
            console.error('Error fetching allocations:', error);
          });
      },
      closePopup() {
        this.showPopup = false;
        this.allocations = [];
      },
      revokeAccess(requestId) {
        fetch(`http://127.0.0.1:5000/revoke_access/${requestId}`, { method: 'POST' })
          .then(response => response.json())
          .then(data => {
            alert(data.message);
            // Refresh allocations
            this.fetchAllocations(this.currentBookId);
          })
          .catch(error => {
            console.error('Error revoking access:', error);
          });
      }
    },
    created() {
      this.fetchBooks(); // Fetch approved books when the component is created
    }
  };
  </script>
  
  <style scoped>
  .book-box {
    border: 1px solid #ddd;
    padding: 15px;
    margin: 15px;
    border-radius: 8px;
    background: #f9f9f9;
    width: 250px; /* Fixed width */
    height: 250px; /* Fixed height */
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .book-details {
    flex: 1;
  }
  
  .book-title, .book-author, .book-category {
    margin: 5px 0;
  }
  
  .book-title {
    font-size: 1.2em;
    font-weight: bold;
    color: #333;
  }
  
  .book-author, .book-category {
    font-size: 1em;
    color: #555;
  }
  
  .view-button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    margin-top: 10px;
  }
  
  .view-button:hover {
    background-color: #0056b3;
  }
  
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .popup-content {
    background: #fff;
    padding: 30px;
    border-radius: 8px;
    width: 80%;
    max-width: 700px;
    position: relative;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .popup-title {
    font-size: 1.5em;
    font-weight: bold;
    color: #333;
  }
  
  .allocation-item {
    margin-bottom: 15px;
  }
  
  .allocation-info {
    font-size: 1.2em;
    color: #555;
  }
  
  .revoke-button {
    background-color: #dc3545;
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
  }
  
  .revoke-button:hover {
    background-color: #c82333;
  }
  
  .close {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 24px;
    color: #333;
    cursor: pointer;
  }
  </style>
  