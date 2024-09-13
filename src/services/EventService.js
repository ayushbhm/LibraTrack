import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000',
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

export default {
  get_book_details() {
    return apiClient.get('/api/admin_get_book_details')
  },

  updateBookDetails(bookId, updatedBookData) {
    const url = `/api/admin_update_book/${bookId}`;
    return apiClient.post(url, updatedBookData)
      .then(response => {
        for (const entry of updatedBookData.entries()) {
          console.log(`${entry[0]}:`, entry[1]);
        }
        return response.data; 
      })
      .catch(error => {
        throw error; 
      });
  },
  getBookCategories() {
    return apiClient.get('/api/admin_get_categories')
  }
,

addBook(bookData) {
  const url = '/add_book';
  return apiClient.post(url, bookData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => {
    return response.data;
  }).catch(error => {
    throw error;
  });
},

adminDeleteBook(bookId) {
  const url = `/admin_delete_book/${bookId}`;
  return apiClient.delete(url)
    .then(response => {
      return response.data;
    })
    .catch(error => {
      throw error;
    });
  



}

}