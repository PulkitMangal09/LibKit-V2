<template>
    <div>
      <MyBooksNav />
      <ul class="nav nav-tabs justify-content-center mt-4">
        <li class="nav-item">
          <router-link :to="{ name: 'MyBooks' }" class="nav-link" active-class="active">Requests</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{ name: 'UserApprovedView' }" class="nav-link" >Approved Books</router-link>
        </li>
      </ul>
  
      <div v-if="error" class="alert alert-danger text-center mt-3" role="alert">
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="container mt-4">
        <div v-if="main_data.length" class="row">
          <div v-for="request in main_data" :key="request.id" class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100 shadow-sm position-relative">
              <div :class="['ribbon', statusRibbonClass(request.status)]">
                <span>{{ request.status }}</span>
              </div>
              <div class="card-body">
                <h5 class="card-title">{{ request.book_title }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">Author: {{ request.book_author }}</h6>
                <p class="card-text">
                  <strong>Section:</strong> {{ request.section }}<br>
                  <strong>Request ID:</strong> {{ request.id }}
                </p>
              </div>
            </div>
          </div>
        </div>
  
        <div v-else class="text-center mt-4">
          <p>No requests found.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import MyBooksNav from '@/components/MyBooksNav.vue';
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  
  const main_data = ref([]);
  const error = ref('');
  const router = useRouter();
  
  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/user_pending_requests', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      main_data.value = response.data;
    } catch (err) {
      if (err.response && err.response.status === 401) {
        router.push({ name: 'login' });
      } else {
        error.value = 'An error occurred while fetching data';
        console.error(err);
      }
    }
  };
  
  // Fetch data from API on component mount
  onMounted(fetchData);
  
  const statusRibbonClass = (status) => {
    switch (status) {
      case 'approved':
        return 'ribbon-success';
      case 'rejected':
        return 'ribbon-danger';
      case 'pending':
        return 'ribbon-warning';
      default:
        return '';
    }
  };
  </script>
  
  <style scoped>
  .nav-tabs {
    justify-content: center;
  }
  
  .nav-link {
    font-size: 1.1rem;
    margin: 0 10px;
  }

  .nav-link.active {
  color: #495057;
  background-color: #e9ecef;
  border-color: #dee2e6 #dee2e6 #fff;
}
  
  .container {
    margin-top: 20px;
  }
  
  .card {
    border-radius: 10px;
    position: relative;
  }
  
  .card-body {
    text-align: center;
  }
  
  .card-title {
    font-size: 1.25rem;
    font-weight: bold;
  }
  
  .card-subtitle {
    font-size: 1rem;
    color: #6c757d;
  }
  
  .card-text {
    font-size: 1rem;
    color: #495057;
  }
  
  .ribbon {
    position: absolute;
    top: -10px;
    right: -10px;
    width: 150px;
    height: 150px;
    overflow: hidden;
  }
  
  .ribbon span {
    position: absolute;
    display: block;
    width: 225px;
    padding: 15px 0;
    background-color: #333;
    color: #fff;
    text-align: center;
    font-size: 0.8rem;
    transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
    box-shadow: 0 3px 10px -5px rgba(0, 0, 0, 1);
  }
  
  .ribbon-success span {
    background-color: #28a745;
  }
  
  .ribbon-danger span {
    background-color: #dc3545;
  }
  
  .ribbon-warning span {
    background-color: #ffc107;
  }
  
  .alert {
    max-width: 600px;
    margin: 0 auto;
  }
  
  .text-center {
    text-align: center;
  }
  
  .mt-4 {
    margin-top: 1.5rem;
  }
  </style>
  