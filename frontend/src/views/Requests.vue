<template>
    <div>
      <RequestsNav />
  
      <!-- Navigation Tabs -->
      <ul class="nav nav-tabs justify-content-center mt-4">
        <li class="nav-item">
          <router-link :to="{ name: 'Requests' }" class="nav-link" active-class="active">Pending Requests</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{ name: 'AdminApprovedBooks' }" class="nav-link">Approved Requests</router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{ name: 'AdminRejectedView' }" class="nav-link">Rejected Requests</router-link>
        </li>
      </ul>
  
      <!-- Alerts -->
      <div v-if="message" class="alert alert-warning alert-dismissible fade show mt-3" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
  
      <div v-if="error" class="alert alert-danger text-center mt-3" role="alert">
        <span>{{ error }}</span>
      </div>
  
      <!-- Request List -->
      <div v-else>
        <div v-if="main_data.length" class="container mt-4">
          <div class="row">
            <div v-for="(request, index) in main_data" :key="index" class="col-md-12 mb-3">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">{{ request.book_title }}</h5>
                  <h6 class="card-subtitle mb-2 text-muted">User: {{ request.user_name }}</h6>
                  <p class="card-text">
                    <strong>Book Author:</strong> {{ request.book_author }}<br>
                    <strong>Section:</strong> {{ request.section }}<br>
                    <strong>Request ID:</strong> {{ request.id }}
                  </p>
                  <div class="d-flex justify-content-between">
                    <button type="button" class="btn btn-success" @click="approveRequest(request.id)">Approve</button>
                    <button type="button" class="btn btn-danger" @click="rejectRequest(request.id)">Reject</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <div v-else class="text-center mt-4">
          <p>No pending requests found.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import RequestsNav from '@/components/RequestsNav.vue';
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  
  const main_data = ref([]);
  const error = ref('');
  const message = ref('');
  const router = useRouter();
  
  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/admin_pending_requests', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      // Convert the response object to an array
      main_data.value = Object.values(response.data);
    } catch (err) {
      if (err.response && err.response.status === 401) {
        router.push({ name: 'login' });
      } else {
        error.value = 'An error occurred. Please try again later.';
        console.error(err);
      }
    }
  };
  
  // Fetch data from API on component mount
  onMounted(fetchData);
  
  const approveRequest = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:5000/admin_approve/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      message.value = response.data.message; // Correctly use the message from the API response
      setTimeout(() => {
        message.value = '';
      }, 3000);

      fetchData(); // Refresh the data
    } catch (err) {
      if (err.response && err.response.data && err.response.data.message) {
        error.value = err.response.data.message; // Use the message from the API error response
        setTimeout(() => {
          error.value = '';
        }, 3000);
      } else {
        error.value = 'An error occurred while approving the request.';
        setTimeout(() => {
          error.value = '';
        }, 3000);
      }
      console.error(err);
    }
  };
  
  const rejectRequest = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:5000/admin_reject/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      message.value = response.data.message; // Correctly use the message from the API response
      setTimeout(() => {
        message.value = '';
      }, 3000);
      fetchData(); // Refresh the data
    } catch (err) {
      if (err.response && err.response.data && err.response.data.message) {
        error.value = err.response.data.message; // Use the message from the API error response
        setTimeout(() => {
          error.value = '';
        }, 3000);

      } else {
        error.value = 'An error occurred while rejecting the request.';
        setTimeout(() => {
          error.value = '';
        }, 3000);
      }
      console.error(err);
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
  

  
  .alert {
    max-width: 600px;
    margin: 0 auto;
  }
  
  .card {
    border-radius: 10px;
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
  
  .btn {
    font-size: 0.9rem;
  }
  
  .d-flex {
    display: flex;
  }
  
  .justify-content-between {
    justify-content: space-between;
  }
  
  .mt-4 {
    margin-top: 1.5rem;
  }
  </style>
  