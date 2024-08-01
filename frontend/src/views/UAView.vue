<template>
    <div class="error-page">
      <img src="@/assets/401.jpeg" alt="Authorization Failed">
      <h1>Oops! Looks like you have entered the wrong room.</h1>
      <h2>Click <router-link to="/">here</router-link> to go back to the home page.</h2>
      <p>Automatic redirecting to login page in {{ seconds }} seconds...</p>
    </div>
  </template>
  
  
<script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import router from '@/router';
  
  const seconds = ref(10);
  
  const countdown = () => {
    if (seconds.value > 0) {
      seconds.value -= 1;
    } else {
      router.push('/login');
    }
  };
  
  let interval;
  onMounted(() => {
    interval = setInterval(countdown, 1000);
  });
  
  onUnmounted(() => {
    clearInterval(interval);
  });
  </script>
  
  <style scoped>
  .error-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    text-align: center;
    background-color: #f9fafc;
    padding: 20px;
    font-family: 'Arial', sans-serif;
  }
  
  img {
    max-width: 600px;
    height: auto;
    object-fit: cover;
    margin-bottom: 20px;
    border-radius: 10px;
    background-color: #f9fafc;
  }
  
  h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    color: #333;
    font-weight: bold;
  }
  
  h2 {
    font-size: 1.5rem;
    color: #666;
    margin-bottom: 20px;
  }
  
  p {
    font-size: 1rem;
    color: #666;
    background-color: #ffefef;
    padding: 10px 20px;
    border-radius: 5px;
    border: 1px solid #ff0000;
  }
  
  a {
    color: #ff0000;
    text-decoration: none;
    font-weight: bold;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>
  