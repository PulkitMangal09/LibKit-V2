<template>
    <div>
      <Navbar/>
      <div v-if="alertMessage" class="alert" :class="alertType" role="alert">
      {{ alertMessage }}
    </div>

      <div id="form-body">
        <h1>User Login</h1>
        <div class="mb-3">
          <label for="uname" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="uname" placeholder="Enter your username" name="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" placeholder="Enter your password" name="password" required>
        </div>
        <div style="text-align:center">
          <button @click="submitLogin" class="btn btn-primary">Login</button><br>
          New User? <router-link to="/register">Register Here</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  
  import { ref } from 'vue';
  import Navbar from '../components/Navbar.vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';

  const username = ref('');
  const password = ref('');
  const router = useRouter();
  const alertMessage = ref('');
  const alertType = ref('');

  const submitLogin = async () => {
    //check if the fields are empty
    if (!username.value || !password.value) {
      showAlert('Please fill in all the fields', 'alert-danger');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/login', {
        username: username.value,
        password: password.value
      });
      // console.log(response.data);
      if (response.data.token){
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user_type', response.data.user_type);
        localStorage.setItem('user_id', response.data.user_id);
        localStorage.setItem('username', response.data.user_name);
        if (response.data.user_type === 'admin'){
          router.push('/admin_dash');
        } else {
          router.push('/user_dash');
      }
    } else {
      showAlert('Invalid username or password', 'alert-danger');
    }


    } catch (error) {
      if (error.response && error.response.data.message) {
      showAlert(error.response.data.message, 'alert-danger');
    } else {
      showAlert('Invalid username or password', 'alert-danger');
    }
    console.error(error);
    }
  }
  
  const showAlert = (message, type) => {
  alertMessage.value = message;
  alertType.value = type;
  setTimeout(() => {
    alertMessage.value = '';
    alertType.value = '';
  }, 3000);
  }

  </script>
  
  <style scoped>
  /* Reset CSS */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  /* Form Body Styles */
  #form-body {
    border: 1px solid red;
    width: 467px;
    height: 349px;
    margin: auto;
    margin-top: 120px;
    border-radius: 10px;
    background-color: white;
    padding: 20px;
  }
  
  /* Margin for form elements */
  .mb-3 {
    margin-bottom: 1rem;
  }
  
  /* Form Label Styles */
  .form-label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  /* Form Input Styles */
  .form-control {
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
  }
  
  /* Button Styles */
  .btn {
    display: inline-block;
    font-weight: 400;
    color: #212529;
    text-align: center;
    vertical-align: middle;
    cursor: pointer;
    background-color: #007bff;
    border: 1px solid #007bff;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    border-radius: 0.25rem;
    color: #fff;
  }
  
  .btn:hover {
    background-color: #0056b3;
    border-color: #004085;
  }

  .alert {
    margin-top: 10px;
    text-align: center;
    padding: 10px;
    border-radius: 5px;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}
  </style>
  