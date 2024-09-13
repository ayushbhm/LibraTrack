<template>
  <div>
    <div
      v-for="(category, index) in categories"
      :key="index"
      class="category-box"
    >
      <div class="category-content">
        <div class="category-title"> <h3>   {{ category.category }}  </h3></div>
        <div class="button-container">
          <button @click="updateCategory(category)">Update</button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-trash"
            viewBox="0 0 16 16"
            @click="deleteCategory(category.id)"
            style="cursor: pointer; margin-left: 5px;"
          >
            <path
              d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"
            />
            <path
              d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"
            />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categories: [],
      token: '' // Add token property to store JWT token
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      // Retrieve JWT token from local storage or wherever you store it
      this.token = localStorage.getItem('token');

      // Make HTTP request to fetch categories data from API
      axios.get('/api/get_book_categories', {
        headers: {
          Authorization: `Bearer ${this.token}` // Send token in Authorization header
        }
      })
        .then(response => {
          // Update categories data
          this.categories = response.data;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
    },
    deleteCategory(id) {
      if (confirm('Are you sure you want to delete this category?')) {
        // Make HTTP request to delete category
        axios.delete(`/api/delete_book_category/${id}`, {
          headers: {
            Authorization: `Bearer ${this.token}` // Send token in Authorization header
          }
        })
          .then(response => {
            // Remove deleted category from the list
            this.categories = this.categories.filter(category => category.id !== id);
          })
          .catch(error => {
            console.error('Error deleting category:', error);
            alert('Failed to delete category');
          });
      }
    },
    updateCategory(category) {
      const newName = window.prompt('Enter new category name:', category.category);
      if (newName !== null) { // Prompt returns null if canceled
        if (newName.trim() === '') {
          alert('Category name cannot be empty');
          return;
        }
        // Make HTTP request to update category
        axios.put(`/api/update_book_category/${category.id}`, {
          category: newName
        }, {
          headers: {
            Authorization: `Bearer ${this.token}` // Send token in Authorization header
          }
        })
          .then(response => {
            // Update category name in the list
            category.category = newName;
          })
          .catch(error => {
            console.error('Error updating category:', error);
            alert('Failed to update category');
          });
      }
    }
  }
};
</script>

<style>
.category-box {
  width: 200px;
  height: 200px; /* Adjust width to make the boxes larger and fit 4 boxes in a row */
  display: inline-block;
  margin-right: 20px; /* Add spacing between boxes */
  margin-bottom: 20px;
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.15);
  border: 1px solid #000;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
}

.category-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.category-title {
  margin-bottom: 10px;
}

.button-container {
  margin-top: auto;
}
</style>
