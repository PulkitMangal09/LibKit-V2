<template>
  <div>
    <SectionViewNav :sectionId="id" />
    <div class="shop-section">
      <div v-for="(book, index) in books" :key="index" class="box1 box">
        <div class="box-content">
          <img :src="getImageUrl(book.image)" alt="No Image Available" @error="handleImageError">
          <div class="text-container">
            <h4 style="text-indent: 100px;">{{ book.title }}</h4>
            <p style="text-indent: 100px;">Author: {{ book.author }}</p>
            <p style="text-indent: 100px;">Content: {{ book.content }}</p>
            <div style="margin-left: 290px;">
              <button type="button" class="btn btn-outline-primary" @click="navigateTo('UpdateBook', book.id)" style="background-color: #3887BE; margin-right: 30px; border-radius: 5px; color:white">Update Book</button>
              <button type="button" class="btn btn-outline" @click="deleteBook(book.id)" style="background-color: #3887BE; margin-right: 30px; border-radius: 5px; color:white">Delete Book</button>
              <button type="button" class="btn btn-outline" @click="navigateTo(book.id)" style="background-color: #3887BE; margin-right: 30px; border-radius: 5px; color:white">View Issued Users</button>
            </div>
          </div>
        </div>
      </div>            
    </div>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import SectionViewNav from '@/components/SectionViewNav.vue';

const route = useRoute();
const router = useRouter();
const id = ref(route.params.id);
const books = ref([]);
const errorMessage = ref('');

const getImageUrl = (image) => `http://localhost:5000/static/images/${image}`;

const handleImageError = (event) => {
  event.target.src = 'http://localhost:5000/static/images/default.jpg';
};

const deleteBook = async (id) => {
  if (!confirm("Are you sure you want to delete this book?")) {
    return; // Cancel deletion if user clicks Cancel in confirmation dialog
  }
  
  try {
    const token = localStorage.getItem('token');
    const response = await axios.delete(`http://localhost:5000/api/${id}/delete_book`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    alert(response.data.message); // Display success message
    await fetchBooks(); // Refresh book list after deletion
  } catch (error) {
    if (error.response && error.response.status === 401) {
      router.push({ name: 'login' });
    } else {
      console.error('Error deleting book:', error);
      alert('Failed to delete book.'); // Display error message
    }
  }
};

const fetchBooks = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get(`http://localhost:5000/api/${id.value}/all_books`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    books.value = Object.values(response.data);
    if (Object.values(response.data).length === 0) {
      errorMessage.value = 'No Books found';
    } else {
      errorMessage.value = '';
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      router.push({ name: 'login' });
    } else {
      console.error(error);
    }
  }
};

onMounted(fetchBooks);

const navigateTo = (routeName, id = null) => {
  if (id) {
    router.push({ name: routeName, params: { id } });
  } else {
    router.push({ name: routeName });
  }
};
</script>


<style scoped>
    .shop-section {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start; /* Updated to align boxes to the left */
    }

    .box {
        height: 220px;
        width: 1300px;
        padding: 20px 0px 15px;
        margin-top: 15px;
        margin-bottom: 10px;
        margin-left: 110px;
        margin-right: 25px; /* Added margin between boxes */
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .box img {
        width: 140px;
        height: 170px;
        margin-left: 50px;
        margin-bottom: 15px;
        background-size: cover;
        background-position: center;
        float: left; /* Added float property to align image to the left */
    }

 
    .box p {
        margin-bottom: 15px;
    }
    .box {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
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