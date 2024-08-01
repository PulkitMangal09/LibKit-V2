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
        <h4 style="text-align: center; color: black;">{{ section.title }}</h4>
        <img :src="getImageUrl(section.image)" alt="No Image Available" @error="handleImageError">
        <p style="text-align: center;">Date: {{ section.date }}</p>
        <p style="text-align:center">Description: {{ section.description }}</p>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
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
const errorMessage = ref('');

const getImageUrl = (image) => `http://localhost:5000/static/images/${image}`;

const handleImageError = (event) => {
  event.target.src = 'http://localhost:5000/static/images/default.jpg';
};


// Fetch data from API on component mount
onMounted(async () => {
  await fetchData();
});

const fetchData = async () => {
  try {
    const token = localStorage.getItem('token');
    //check if token is available
    if (!token) {
      router.push({ name: 'UAView' });
    }

    const response = await axios.get('http://localhost:5000/api/all_sections', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    sections.value = response.data;
    if(Object.values(response.data).length === 0) {
      errorMessage.value = 'No sections found';
    }
    else {
      errorMessage.value = '';
    }

  } catch (error) {
    if (error.response && error.response.status === 401) {
      router.push({ name: 'UAView' });
    } else {
      console.error(error);
      router.push({ name: 'UAView' });
    }
  }
};

const goToSection = (id) => {
  router.push({ name: 'SectionView', params: { id } });
};


</script>

<style scoped>
.shop-section {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.box {
  height: auto; /* Adjust height as needed */
  width: 330px;
  padding: 20px 0px 15px;
  margin-top: 10px;
  margin-bottom: 25px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Ensures content is evenly spaced */
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
  border-radius: 5px; /* Add border-radius for images */
}

.box p {
  text-align: center;
  color: black;
  margin: 5px 0;
}

.box-content {
  flex: 1; /* Fill remaining space within the box */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.error-message {
  position: fixed;
  left: 50%;
  margin-top: 300px;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 1000;
  width: fit-content;
  color: #721c24;
  font: 2em sans-serif;
}


</style>
