<template>
  <div>
    <svg @click="confirmDelete" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
      <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
    </svg>

    <div v-if="showConfirm" class="confirm-popup">
      <p>Are you sure you want to delete this book?</p>
      <button @click="deleteBook">Yes</button>
      <button @click="cancelDelete">No</button>
    </div>
  </div>
</template>

<script>
import EventService from '@/services/EventService.js';

export default {
  props: {
    bookId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      showConfirm: false
    };
  },
  methods: {
    confirmDelete() {
      this.showConfirm = true;
    },
    cancelDelete() {
      this.showConfirm = false;
    },
    deleteBook() {
      EventService.adminDeleteBook(this.bookId)
        .then(() => {
          this.$emit('bookDeleted');
          this.showConfirm = false;
        })
        .catch(error => {
          console.error('Error deleting book:', error);
        });
    }
  }
};
</script>

<style scoped>
.confirm-popup {
  width: 300px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.confirm-popup p {
  margin-bottom: 20px;
  color: black;
}

.confirm-popup button {
  margin: 5px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.confirm-popup button:first-of-type {
  background-color: #e74c3c;
  color: white;
}

.confirm-popup button:last-of-type {
  background-color: #3498db;
  color: white;
}
</style>
