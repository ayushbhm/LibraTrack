<template>
  <nav class="navbar navbar-expand-lg bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand text-light" href="<">Navbar</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link active text-light" aria-current="page" to="/StudentHome">Home</router-link>
          </li>
          <li>
            <router-link class="nav-link active text-light" aria-current="page" to="/StudentBooks">MyBooks</router-link>
          </li>
        </ul>
        <form v-if="isHomeView" class="d-flex" role="search" @submit.prevent="emitSearch">
          <input
            class="form-control me-2 bg-dark text-light border border-success"
            type="search"
            placeholder="Search"
            aria-label="Search"
            v-model="searchQuery"
            @input="emitSearch"
          />
         <UserProfileVue/>
        </form>
      </div>
    </div>
  </nav>
</template>

<script>
import UserProfileVue from './UserProfile.vue';

export default {
  components :{
    UserProfileVue
  },
  data() {
    return {
      searchQuery: ''
    }
  },
  computed: {
    isHomeView() {
      return this.$route.name === 'home'; // Assuming 'home' is the name of your HomeView route
    }
  },

  methods: {
    emitSearch() {
      this.$emit('search', this.searchQuery)
    }
  }
}
</script>
