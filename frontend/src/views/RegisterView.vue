<template>
    <div>
      <Navbar/>
      <div v-if="alertMessage" class="alert" :class="alertType" role="alert">
                {{ alertMessage }}
        </div>
  
      <div id="form-body">
        
        <h1>User Sign in</h1>
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input v-model="name" type="text" class="form-control" id="name" placeholder="Enter your Name" name="name" required>
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="username" placeholder="Enter your Username" name="username" required>
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input v-model="email" type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter your email" name="email" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" placeholder="Enter your password" name="password" required>
        </div>
        <div style="text-align:center">
          <button @click="submitInfo" class="btn btn-primary">Sign in</button><br>
          <br>
          Already have an account? <router-link to="/login">Login Here</router-link>
        </div>
   
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import Navbar from '../components/Navbar.vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';

  const name = ref('');
  const username = ref('');
  const email = ref('');
  const password = ref('');
  const router = useRouter();
  const alertMessage = ref('');
  const alertType = ref('');

  const submitInfo = async () =>{

    try{

      const response = await axios.post('http://localhost:5000/register', {
            name: name.value,
            username: username.value,
            email: email.value,
            password: password.value
        });
        router.push('/login');

    }
    catch(error){
      if (error.response && error.response.data.message){
        // Display error message
        showAlert(error.response.data.message, 'alert-danger');
      }
      else{
        // Generic error message
        showAlert('Failed to register. Please try again.', 'alert-danger');
      }
    }

  }

  const showAlert = (message, type) => {
    alertMessage.value = message;
    alertType.value = type;
    // Clear alert after a few seconds
    setTimeout(() => {
        alertMessage.value = '';
        alertType.value = '';
    }, 3000); // 3000 milliseconds = 3 seconds
  }
  
  

  </script>
  
  <style scoped>
  /* Reset CSS */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  /* Global Styles */
  body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
  }
  
  /* Form Body Styles */
  #form-body {
    border: 1px solid red;
    width: 490px;
    height: 548px;
    margin: 50px auto 0;
    border-radius: 10px; /* Rounded corners */
    background-color: white;
    padding: 20px; /* Add padding inside the form body */
  }
  
  /* Form Element Styles */
  .form-label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-control {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  /* Button Styles */
  .btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  /* Link Styles */
  a {
    color: #007bff;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  /* Centered Text */
  .text-center {
    text-align: center;
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
  