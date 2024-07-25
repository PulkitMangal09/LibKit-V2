<template>
    <div>
      <RequestsNav />
  
      <!-- Navigation Tabs -->
      <ul class="nav nav-tabs justify-content-center mt-4">
        <li class="nav-item">
          <router-link :to="{ name: 'Requests' }" class="nav-link" >Pending Requests</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{ name: 'AdminApprovedBooks' }" class="nav-link" >Approved Requests</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{ name: 'AdminRejectedView' }" class="nav-link" active-class="active">Rejected Requests</router-link>
        </li>
      </ul>
  
      <!-- Flash messages -->
      <div v-if="flashMessage" class="alert alert-warning alert-dismissible fade show" role="alert">
        {{ flashMessage }}
        <button type="button" class="btn-close" @click="flashMessage = ''" aria-label="Close"></button>
      </div>
  
      <!-- Error message -->
      <div v-if="error" class="alert alert-danger text-center" role="alert">
        <span>{{ error }}</span>
      </div>
  
      <!-- Requests Display -->
      <div class="requests-container">
        <div v-if="requests.length" class="requests-list">
          <div v-for="(request, index) in requests" :key="index" class="request-card">
            <div class="request-details">
              <h5>Request ID: {{ request.id }}</h5>
              <p><strong>User ID:</strong> {{ request.user_id }}</p>
              <p><strong>User Name:</strong> {{ request.user_name }}</p>
              <p class="book-title"><strong>Book Title:</strong> {{ request.book_title }}</p>
              <p class="book-title"><strong>Book Author:</strong> {{ request.book_author }}</p>
              <p class="book-title"><strong>Book Section:</strong> {{ request.section }}</p>
            </div>
          </div>
        </div>
        <div v-if="!requests.length" class="no-requests">
          <p>No requests to display.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import RequestsNav from '@/components/RequestsNav.vue';
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';


  const router = useRouter();
  const requests = ref([]);
  const flashMessage = ref('');
  const error = ref('');
  
  const fetchRequests = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/admin_rejected_books', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
      requests.value = Object.values(response.data);
    } catch (err) {
      if (err.response && err.response.status === 401) {
          router.push({ name: 'UAView' });
        } else {
          error.value = 'An error occurred. Please try again later.';
          console.error(err);
        }
    }
  };
  
  
  
  onMounted(fetchRequests);
  </script>
  
  <style scoped>
  .alert {
    margin-top: 10px;
  }
  
  .requests-container {
    padding: 20px;
  }
  
  .requests-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .request-card {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
    width: calc(33.333% - 20px);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .request-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }
  
  .request-details h5 {
    font-size: 1.2rem;
    margin-bottom: 10px;
  }
  
  .request-details p {
    margin: 5px 0;
  }
  
  .book-title {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }
  
  .btn-danger {
    background-color: #dc3545;
    border: none;
    color: #fff;
    padding: 10px;
    font-size: 0.875rem;
  }
  
  .no-requests {
    text-align: center;
    margin-top: 20px;
    font-size: 1.2rem;
    color: #666;
  }
  </style>
  