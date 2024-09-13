<script setup>
import { ref } from 'vue';

import Studentnavbar from '../components/Studentcomponents/Studentnavbar.vue';
import BookBox from '../components/Studentcomponents/AllBooksBox.vue';
import BooksStatusBox from '../components/Studentcomponents/PendingBooksBox.vue';
import ApprovedBooksVue from '../components/Studentcomponents/ApprovedBooks.vue';

const searchQuery = ref('');

const updateSearchQuery = (query) => {
  searchQuery.value = query;
};
</script>

<template>
  <main>
    <Studentnavbar @search="updateSearchQuery" />
    <h2>All Books</h2>
    <BookBox :search-query="searchQuery" />
    <h2>My Approved Books</h2>
    <ApprovedBooksVue />
  </main>
</template>
