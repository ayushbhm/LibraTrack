<script setup> 
import StudentNavbar from '../components/Studentcomponents/Studentnavbar.vue'
import ApprovedBooksVue from '../components/Studentcomponents/ApprovedBooks.vue'
import PendingBooksBox from '@/components/Studentcomponents/PendingBooksBox.vue';

import RejectedBooksBoxVue from '@/components/Studentcomponents/RejectedBooksBox.vue';
</script>


<template>
    <StudentNavbar/>
    
    <ApprovedBooksVue/>
  
    <PendingBooksBox />
   
    <RejectedBooksBoxVue />

</template>