<template>
 <div>
    <UserNav />
    
    <main class="main">
      <br>
      <section class="book-grid">
        <article class="book" v-for="(book, index) in books" :key="book.id">
          <div class="book-content">
            <div class="image-container">
              <img :src="getImageUrl(book.image)" alt="No Image Available" @error="handleImageError">
            </div>
            <div class="text-container">
              <h4>{{ book.title }}</h4>
              <p>by {{ book.author }}</p>
              <p>{{ book.section }}</p>
              <div class="rating">
                <span v-for="star in getStarRating(book.rating)" :key="star" class="star">&#9733;</span>
              </div>
            </div>
            <div class="button-container">
              <button type="button" class="btn btn-outline-info" @click="borrowBook(book.id)">Borrow Book</button>
            </div>
          </div>  
        </article>
      </section>
    </main>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import UserNav from '@/components/UserNav.vue';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const books = ref([]);
const router = useRouter();
const successMessage = ref('');
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
    const response = await axios.get('http://localhost:5000/user', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    books.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      router.push({ name: 'login' });
    } else {
      console.error(error);
    }
  }
};

const borrowBook = async (id) => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get(`http://localhost:5000/userborrow/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    successMessage.value = response.data.message;
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
    await fetchData();
  } catch (error) {
    if (error.response) {
      if (error.response.status === 401) {
        router.push({ name: 'login' });
      } else {
        errorMessage.value = error.response.data.message;
        setTimeout(() => {
          errorMessage.value = '';
        }, 3000);
      }
    } else {
      console.error(error);
    }
  }
};

const getStarRating = (rating) => {
  const stars = [];
  for (let i = 0; i < rating; i++) {
    stars.push(i);
  }
  return stars;
};

</script>

<style scoped>
html, body {
  height: 100%;
  margin: 0;
  font-family: 'Roboto', sans-serif;
}

body {
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  padding: 20px;
  background-color: #f8f9fa;
 
}

.book-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  padding: 20px;
  justify-content: center;
}

.book {
  width: calc(33.333% - 60px);
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 450px;
}

.book:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.book-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  flex: 1;
}

.image-container {
  width: 50%;
  height: 250px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.text-container {
  text-align: center;
  margin-top: 15px;
}

.text-container h4 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.text-container p {
  font-size: 1rem;
  margin: 0.25rem 0;
  color: #666;
}

.rating {
  margin-top: 10px 0;
}

.star {
  color: #f1c40f;
  font-size: 1.5rem;
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin-top: auto;
}

.btn {
  padding: 10px 20px;
  font-size: 0.875rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #0056b3;
}

.success-message, .error-message {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 1000;
  width: fit-content;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

@media (max-width: 768px) {
  .book {
    width: calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .book {
    width: 100%;
  }
}
</style>

