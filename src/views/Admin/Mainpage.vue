<script >

import CategoryBoxVue from "@/components/Admin/CategoryBox.vue";
import AdminNavbar from "@/components/Admin/AdminNavbar.vue"
import BookRequestButton from "@/components/Admin/BookRequestButton.vue"
import AdminApprovedBooks from "@/components/Admin/AdminApprovedBooks.vue";
export default{
    components : {
        BookRequestButton,
        AdminNavbar,
        AdminApprovedBooks
    }
};


</script>

<template>
    <AdminNavbar/>
    New Book Requests

    <BookRequestButton/>
    <br>
    <br>
    Approved Books
    <AdminApprovedBooks/>

    
</template>