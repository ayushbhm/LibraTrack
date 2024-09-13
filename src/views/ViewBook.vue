<script setup> 
import ReviewBookBox from '../components/Studentcomponents/ReviewBookBox.vue'
</script>
<template>

    <div>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <div v-if="pdfData">
            <center> <iframe :src="pdfData" width="800px" height="700px"></iframe> </center>
          
        </div>
        <div v-else>No PDF available</div>
      </div>

     <center > <ReviewBookBox :bookId="$route.params.bookId" /> </center>
      
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        pdfData: null,
        loading: false
      }
    },
    mounted() {
      this.getBookPdf()
    },
    methods: {
      async getBookPdf() {
        this.loading = true
        const bookId = this.$route.params.bookId // Assuming bookId is passed as a route parameter
        try {
          const response = await axios.get(`/api/get_book_pdf/${bookId}`)
          this.pdfData = `data:application/pdf;base64,${response.data}` // Construct data URI
        } catch (error) {
          console.error('Error fetching book PDF:', error)
        } finally {
          this.loading = false
        }
      }
    }
  }
  </script>
  
  <style>


  
  </style>
  