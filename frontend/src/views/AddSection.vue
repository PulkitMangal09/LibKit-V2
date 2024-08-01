<template>
    <div>
      <AddSectionNav />
      <br />
      <div class="container">
        <div class="box">
          <div class="form-group">
            <label for="title" class="form-label">Section Title</label>
            <input type="text" class="form-control" id="title" placeholder="Enter Section Title" v-model="title" required />
          </div>
          <div class="form-group">
            <label for="image" class="form-label">Image Name</label>
            <input type="text" class="form-control" id="image"  placeholder="Enter image name" v-model="image" />
          </div>
          <div class="form-group">
            <label for="description" class="form-label">Description</label>
            <input type="text" class="form-control" id="description" placeholder="Enter the Description of the Section" v-model="description" required />
          </div>
          <div class="form-group">
            <div class="d-flex justify-content-end" style="margin-right: 50px;">
              <button  class="btn btn-outline cancel" @click="navigateTo('AdminDash')">Cancel</button>
              <button class="btn btn-outline add-section" @click="addSection">Add Section</button>
            </div>
          </div>
        </div>
      </div>
      <transition name="fade">
      <div v-if="message" class="message error">
        {{ message }}
      </div>
    </transition>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import AddSectionNav from '../components/AddSectionNav.vue';
  
  const title = ref('');
  const image = ref('');
  const description = ref('');
  const router = useRouter();
  const message= ref('');
  const messageType = ref('info'); 
  
  const addSection = async () => {

    //check if the fields are empty
    if (!title.value || !description.value) {
      message.value = 'Please fill in all the fields.';
      messageType.value = 'error';
      setTimeout(() => {
        message.value = '';
      }, 3000);
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:5000/api/create_section', {
        title: title.value,
        image: image.value,
        description: description.value,
        

      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      // console.log(response.data);
      router.push('/admin_dash');
    } catch (error) {
    if (error.response && error.response.status === 401) {
      router.push({ name: 'UAView' });
    } else {
      console.error(error);
      message.value= response.data.message;
      messageType.value = 'error';
      setTimeout(() => {
        message.value = '';
      }, 3000);
    }
    }
  };
  
  const navigateTo = (routeName) => {
    router.push({ name: routeName });
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    justify-content: center;
  }
  
  .box {
    width: 400px;
    background-color: #f5f7f8;
    padding: 20px;
    margin-top: 50px;
    border-radius: 10px;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .btn-outline {
    background-color: transparent;
    border: 1px solid transparent;
    padding: 10px 20px;
    margin-right: 10px;
    color: #333;
  }
  
  .btn-outline.cancel {
    color: #f04949;
    border-color: #f04949;
  }
  
  .btn-outline.add-section {
    color: forestgreen;
    border-color: forestgreen;
  }
  
  .btn-outline:hover {
    background-color: #e3e3e3;
  }
  
  .btn-outline.cancel:hover {
    color: #fff;
    background-color: #f04949;
    border-color: #f04949;
  }
  
  .btn-outline.add-section:hover {
    color: #fff;
    background-color: forestgreen;
    border-color: forestgreen;
  }

  .message {
  position: fixed;
  top: 100px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 1000;
  width: fit-content;
  border: 1px solid #c3e6cb;
  transition: opacity 0.5s ease;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border-color: #f5c6cb;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}


  </style>
  