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
              <button class="btn btn-outline add-section" @click="updateSection">Update Section</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter,useRoute } from 'vue-router';
  import AddSectionNav from '../components/AddSectionNav.vue';
  
  const title = ref('');
  const image = ref('');
  const description = ref('');
  const router = useRouter();
  const route = useRoute();
  const sectionId = ref(route.params.id);


    const updateSection = async () => {
        try {
        const token = localStorage.getItem('token');
        const response = await axios.put(`http://localhost:5000/api/${sectionId.value}/update_section`, {
            title: title.value,
            image: image.value,
            description: description.value
        }, {
            headers: {
            Authorization: `Bearer ${token}`
            }
        });
        console.log(response.data);
        router.push('/admin_dash');
        } catch (error) {
        if (error.response && error.response.status === 401) {
          router.push({ name: 'UAView' });
        } else {
        console.error(error);
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
  </style>
  