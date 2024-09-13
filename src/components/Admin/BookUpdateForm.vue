<template>
    <div class="update-form">
      <h2>Update Book</h2>
      <form @submit.prevent="updateBook">
        <label for="title">Titldrge:</label>
        <input type="text" id="title" v-model="updatedBook.title" required>
  
        <label for="author">Author:</label>
        <input type="text" id="author" v-model="updatedBook.author" required>
  
        <label for="category">Category:</label>
        <input type="text" id="category" v-model="updatedBook.category" required>

        <button type="submit">Update</button>
        <button type="button" @click="closeForm">Cancel</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      book: Object // Receive entire book object as prop from parent component
    },
    data() {
      return {
        updatedBook: { ...this.book } // Clone selected book for form data
      };
    },
    methods: {
      updateBook() {
        // Implement update book logic using EventService
        // Example:
        // EventService.updateBookDetails(this.book.id, this.updatedBook)
        //   .then(() => {
        //     this.$emit('closeForm'); // Emit event to close the form
        //   })
        //   .catch(error => {
        //     console.error('Error updating book:', error);
        //   });
      },
      closeForm() {
        this.$emit('closeForm'); // Emit event to close the form
      }
    }
  };
  </script>
  
  <style scoped>
  .update-form {
    background-color: #2d2339;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  input {
    width: 100%;
    margin-bottom: 10px;
  }
  </style>
  