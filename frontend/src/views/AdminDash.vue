<template>
    <div>
      <AdminNav />
      <br>
      <h1 style="text-align: center;">Welcome to the Librarian's Dashboard</h1>
      <br />
      <h3 style="text-align: center;">Here you can manage the books and the users</h3>
      <br />
  
      <!-- Displaying sections from API -->
      <div class="shop-section">
        <div v-for="(section, index) in sections" :key="section.id" @click="goToSection(section.id)" class="box1 box">
            <div class="box-content"></div>
            <h4 style="text-align: center; color: black; ">{{ section.title }}</h4>
            <!-- <img :src="(`@/assets/${section.image}`)" alt="No Image Available" @error="handleImageError"> -->
            <p style="text-align: center;">Date: {{ section.date }}</p>
            <p style="text-align:center">Description: {{ section.description }}</p>
          </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import AdminNav from '../components/AdminNav.vue';
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const sections = ref([]);
  const router = useRouter();
  
  // Fetch data from API on component mount
  onMounted(async () => {
    await fetchData();
  });
  
  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/all_sections', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
      sections.value = response.data;
    } catch (error) {
      if (error.response && error.response.status === 401) {
      router.push({ name: 'login' });
    } else {
      console.error(error);
    }
    }
  };
  
  const goToSection = (id) => {
  router.push({ name: 'SectionView', params: { id } });
  };


  const handleImageError = (event) => {
    event.target.src = '@/assets/no-image.png';
  };
  </script>
  
  <style scoped>
  .shop-section {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
  }
  
  .box {
    height: 430px;
    width: 330px;
    padding: 20px 0px 15px;
    margin-top: 10px;
    margin-bottom: 25px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    transition: transform 0.3s ease;
  }
  
  .box:hover {
    transform: scale(1.05);
  }
  
  .box img {
    width: 300px;
    height: 250px;
    margin: 13px;
    margin-bottom: 15px;
    background-size: cover;
    background-position: center;
  }
  
  .box p {
    margin-top: auto;
    text-align: center;
    color: black;
  }
  </style>
  