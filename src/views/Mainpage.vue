<template>
  <div>
    <form @submit.prevent="login" style="width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #444; border-radius: 5px; background-color: #333;">
      <label for="username" style="display: block; margin-bottom: 10px; color: #fff;">Username:</label>
      <input type="text" id="username" v-model="username" style="width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #444; border-radius: 5px; box-sizing: border-box; background-color: #444; color: #fff;" required>

      <label for="password" style="display: block; margin-bottom: 10px; color: #fff;">Password:</label>
      <input type="password" id="password" v-model="password" style="width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #444; border-radius: 5px; box-sizing: border-box; background-color: #444; color: #fff;" required>

      <input type="submit" value="Login" style="width: 100%; padding: 10px; border: none; border-radius: 5px; background-color: #007bff; color: #fff; cursor: pointer;">                              
      New User?  <router-link  to='/RegisterUser'>   Register Here   </router-link>  
    </form>

 
  </div>

  <router-link  to='/AdminLogin'>    Admin Login </router-link>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: this.username,
          password: this.password
        });
        const token = response.data.token;
        localStorage.setItem('token', token);
        this.$router.push('/StudentHome');
        // Do something with the token, such as storing it in localStorage
        console.log('Token:', token);
        // Redirect the user or perform other actions based on successful login
      } catch (error) {
        console.error('Login failed:', error.response.data.message);
        // Handle login failure, display error message to the user, etc.
      }
    }
  }
};
</script>

<style>
body {
  background-image: url('../assets/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
