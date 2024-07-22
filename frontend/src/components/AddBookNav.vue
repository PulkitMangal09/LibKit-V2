<template>
    <header>
      <nav class="navbar navbar-default" style="background-color: #7FC7D9; padding: 0px;">
        <div class="container-fluid">
          <div class="navbar-header">
            <router-link class="navbar-brand" :to="{ name: 'AdminDash' }" style="font-size: 28px;">
              <span style="font-family: Zapfino; font-style: italic; color: white; margin-left: 30px;" ><strong>LibKit</strong></span>
            </router-link>
          </div>
          <div class="container-fluid col-md-3" style="margin-left: 200px;">
            <form class="d-flex" role="search" @submit.prevent="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
              <button type="submit">Filter</button>
            </form>
          </div>
          <ul class="nav navbar-nav navbar-right">
            <li>
              <div class="btn-group">
                <button class="btn  btn-outline navbar-btn" @click="navigateTo('AdminDash')" style=" border-radius: 5px; ">Home</button>
                <button class="btn btn-outline  navbar-btn" @click="navigateTo('UpdateSection',sectionId)" style=" border-radius: 5px;">Update Section</button>
                <button class="btn btn-outline navbar-btn" @click="deleteSection(sectionId)" style="border-radius: 5px;">Delete Section</button>
                <button class="btn btn-outline navbar-btn" @click="logout" style="border-radius: 5px;">Logout</button>
              </div>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  </template>
  
  <script setup>
  import router from '@/router';
  import axios from 'axios';
  import { ref } from 'vue';
  

  const props = defineProps({
    sectionId: {
      type: String,
      required: true
    }
  });
  
  const searchQuery = ref('');

  const logout = () => {
  localStorage.removeItem('token');
  router.push({ name: 'login' });
};
  
  const deleteSection = async (id) => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.delete(`http://localhost:5000/api/${id}/delete_section`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    alert(response.data.message); // Display success message
    // Optionally, update section list or navigate back to AdminDash
    navigateTo('AdminDash');
  } catch (error) {
    console.error('Error deleting section:', error);
    alert('Failed to delete section.'); // Display error message
  }
};

  const navigateTo = (routeName, id = null) => {
    if (id) {
      router.push({ name: routeName, params: { id } });
    } else {
      router.push({ name: routeName });
    }
  };
  
  const search = () => {
    console.log('Searching for:', searchQuery.value);
  };
  </script>
  
  

  <style scoped>

  .btn-outline {
    background-color: transparent;
    color: white;
    border: 1px solid #7FC7D9;
    margin-right: 30px;
  }
  
  .btn-outline:hover {
    background-color: #3887BE;
    color: #fff;
  }
  </style>
  