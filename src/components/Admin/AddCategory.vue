<template>
    <div style="text-align: center; margin-top: 20px;">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="32"
        height="32"
        fill="currentColor"
        class="bi bi-plus-circle"
        viewBox="0 0 16 16"
        style="cursor: pointer;"
        @click="addNewCategory"
      >
        <path
          d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"
        />
        <path
          d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"
        />
      </svg>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    methods: {
      addNewCategory() {
        const categoryName = window.prompt('Enter new category name:');
        if (categoryName && categoryName.trim() !== '') {
          axios.post('/api/add_book_category', { category: categoryName })
            .then(response => {
              console.log('New category added:', response.data.message);
              // Optionally, you can emit an event to notify the parent component
              // about the addition of a new category
            })
            .catch(error => {
              console.error('Error adding category:', error.response.data.error);
            });
        } else {
          console.log('Operation canceled or empty category name entered');
        }
      }
    }
  };
  </script>
  
  <style>
  /* Additional styling can be added here if needed */
  </style>
  