<template>
  <div class="book-box">
    <div v-for="book in books" :key="book.id" class="book-item">
      <h2>{{ book.title }}</h2>
      <p><strong>Author:</strong> {{ book.author }}</p>
      <p><strong>Category:</strong> {{ book.category }}</p>
      <button @click="openUpdateForm(book)">Update</button>
      <div v-if="selectedBook && selectedBook.id === book.id" class="update-form">
        <h2>Update Book</h2>
        <form @submit.prevent="updateBook">
          <label for="title">Title:</label>
          <input type="text" id="title" v-model="updatedBook.title" required />

          <label for="author">Author:</label>
          <input type="text" id="author" v-model="updatedBook.author" required />

          <label for="category">Category:</label>
          <select v-model="updatedBook.category" required>
            <option v-for="category in categories" :key="category.id" :value="category.category">
              {{ category.category }}
            </option>
          </select>

          <button type="submit">Update</button>
          <button type="button" @click="closeUpdateForm">Cancel</button>
        </form>
      </div>
      <delete-book-button :bookId="book.id" @bookDeleted="fetchBooks" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import DeleteBookButton from '@/components/Admin/DeleteBookButton.vue';

export default {
  components: {
    DeleteBookButton
  },
  data() {
    return {
      books: [],
      selectedBook: null,
      updatedBook: {
        id: null,
        title: "",
        author: "",
        category: ""
      },
      categories: []
    };
  },
  created() {
    this.fetchBooks();
    this.fetchCategories();
  },
  methods: {
    fetchBooks() {
      axios.get('http://127.0.0.1:5000/api/get_books_without_pdf')
        .then(response => {
          console.log('Books fetched:', response.data); // Debugging statement
          this.books = response.data;
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    },
    fetchCategories() {
      axios.get('http://127.0.0.1:5000/api/get_book_categories')
        .then(response => {
          console.log('Categories fetched:', response.data); // Debugging statement
          this.categories = response.data;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
    },
    openUpdateForm(book) {
      console.log('Opening update form for book:', book); // Debugging statement
      this.selectedBook = book;
      this.updatedBook = { ...book };
    },
    updateBook() {
      // Validate form fields
      if (!this.updatedBook.title || !this.updatedBook.author || !this.updatedBook.category) {
        alert('Please fill in all required fields.');
        return;
      }

      // Log updatedBook state
      console.log('Updated book data:', this.updatedBook); // Debugging statement

      // Create FormData object and append form data
      let formData = new FormData();
      formData.append('title', this.updatedBook.title);
      formData.append('author', this.updatedBook.author);
      formData.append('category', this.updatedBook.category);

      // Log FormData object
      console.log('FormData object:', formData); // Debugging statement

      // Call API to update book details
      axios.post(`http://127.0.0.1:5000/api/update_book/${this.selectedBook.id}`, formData)
        .then(response => {
          console.log('Update book response:', response.data); // Debugging statement
          this.closeUpdateForm();
          this.fetchBooks(); // Refresh book list after update
        })
        .catch(error => {
          console.error('Error updating book:', error);
        });
    },
    closeUpdateForm() {
      this.selectedBook = null;
      this.updatedBook = {
        id: null,
        title: "",
        author: "",
        category: ""
      };
    }
  }
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
}
</style>
