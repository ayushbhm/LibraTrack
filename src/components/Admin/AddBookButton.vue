<template>
    <div>
      <button @click="openPopup">Add New Book</button>
  
      <div v-if="isPopupOpen" class="update-form">
        <div class="popup-content">
          <span class="close" @click="closePopup">&times;</span>
          <h2>Add New Book</h2>
          <form @submit.prevent="submitBook">
            <div>
              <label for="title">Title:</label>
              <input type="text" id="title" v-model="title" required>
            </div>
            <div>
              <label for="author">Author:</label>
              <input type="text" id="author" v-model="author" required>
            </div>
            <div>
              <label for="category">Category:</label>
              <select id="category" v-model="category" required>
                <option v-for="cat in categories" :key="cat.category" :value="cat.category">
                  {{ cat.category }}
                </option>
              </select>
            </div>
            <div>
              <label for="file">PDF File:</label>
              <input type="file" id="file" accept="application/pdf" @change="handleFileUpload" required>
            </div>
            <button type="submit">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import EventService from '@/services/EventService.js';
  
  export default {
    setup() {
      const isPopupOpen = ref(false);
      const title = ref('');
      const author = ref('');
      const category = ref('');
      const categories = ref([]);
      const selectedFile = ref(null);
  
      const openPopup = () => {
        isPopupOpen.value = true;
      };
  
      const closePopup = () => {
        isPopupOpen.value = false;
        resetForm();
      };
  
      const resetForm = () => {
        title.value = '';
        author.value = '';
        category.value = '';
        selectedFile.value = null;
      };
  
      const handleFileUpload = (event) => {
        selectedFile.value = event.target.files[0];
      };
  
      const fetchCategories = async () => {
        try {
          const response = await EventService.getBookCategories();
          categories.value = response.data;
        } catch (error) {
          console.error('Error fetching categories:', error.response ? error.response.data : error.message);
        }
      };
  
      const submitBook = async () => {
        if (selectedFile.value) {
          const formData = new FormData();
          formData.append('title', title.value);
          formData.append('author', author.value);
          formData.append('category', category.value);
          formData.append('file', selectedFile.value);
  
          try {
            const response = await EventService.addBook(formData);
            console.log('Book added successfully:', response);
            closePopup();
          } catch (error) {
            console.error('Error adding book:', error.response ? error.response.data : error.message);
          }
        } else {
          alert('Please select a PDF file.');
        }
      };
  
      onMounted(() => {
        fetchCategories();
      });
  
      return {
        isPopupOpen,
        title,
        author,
        category,
        categories,
        selectedFile,
        openPopup,
        closePopup,
        handleFileUpload,
        submitBook,
      };
    },
  };
  </script>
  
  <style scoped>
  .book-box {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    margin-top: 20px;
  }
  
  .book-item {
    width: 30%;
    margin-bottom: 20px;
    background-color: rgba(255, 255, 255, 0.15);
    border: 1px solid #000;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
  }
  
  .book-item h2 {
    font-size: 24px;
  }
  
  .book-item p {
    font-size: 16px;
    text-align: left;
    margin-top: 10px;
    color: aliceblue;
  }
  
  button {
    margin-top: 10px;
    cursor: pointer;
  }
  
  .update-form {
    width: 300px;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #281e33;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  input,
  select {
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
    box-sizing: border-box;
  }
  </style>
  