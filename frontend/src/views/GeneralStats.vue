<template>
    <div>
      <GeneralStatsNav />
      <div class="container">
        <h1>Library Statistics</h1>
        <div class="stats">
          <div class="stat total-books">
            <h2>Total Books</h2>
            <p>{{ stats.total_books }}</p>
          </div>
          <div class="stat total-sections" @click="navigateTo('AdminDash')">
            <h2>Total Sections</h2>
            <p>{{ stats.total_sections }}</p>
          </div>
          <div class="stat total-users">
            <h2>Total Users</h2>
            <p>{{ stats.total_users }}</p>
          </div>
          <div class="stat total-requests" @click="navigateTo('Requests')">
            <h2>Total Requests</h2>
            <p>{{ stats.total_requests }}</p>
          </div>
          <div class="stat approved-requests" @click="navigateTo('AdminApprovedBooks')">
            <h2>Approved Requests</h2>
            <p>{{ stats.total_approved_requests }}</p>
          </div>
          <div class="stat rejected-requests" @click="navigateTo('AdminRejectedView')">
            <h2>Rejected Requests</h2>
            <p>{{ stats.total_rejected_requests }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import GeneralStatsNav from '@/components/GeneralStatsNav.vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const stats = ref({});
  const router = useRouter();

  const navigateTo = (routeName) => {
  router.push({ name: routeName });
    };
  
  onMounted(() => {
    axios.get('http://localhost:5000/stats', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then(response => {
      stats.value = response.data;
    })
    .catch(error => {
      console.log(error);
      router.push('/login');
    });
  });
  </script>
  
  <style scoped>
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 0;
  }
  
  .container {
    max-width: 1000px;
    margin: 50px auto;
    padding: 20px;
    background-color: #ffffff;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
  }
  
  h1 {
    text-align: center;
    color: #333333;
  }
  
  .stats {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .stat {
    flex: 1 1 45%;
    margin: 10px;
    padding: 20px;
    text-align: center;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .stat:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  }
  
  .stat h2 {
    margin: 0 0 10px;
    color: #ffffff;
  }
  
  .stat p {
    margin: 0;
    font-size: 2em;
    color: #ffffff;
  }
  
  .total-books {
    background: linear-gradient(135deg, #ff9800, #ff5722);
  }
  
  .total-sections {
    background: linear-gradient(135deg, #3f51b5, #2196f3);
  }
  
  .total-users {
    background: linear-gradient(135deg, #4caf50, #8bc34a);
  }
  
  .total-requests {
    background: linear-gradient(135deg, #e91e63, #f44336);
  }
  
  .approved-requests {
    background: linear-gradient(135deg, #00bcd4, #009688);
  }
  
  .rejected-requests {
    background: linear-gradient(135deg, #9c27b0, #673ab7);
  }
  </style>
  