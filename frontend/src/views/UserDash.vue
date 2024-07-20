<template>
  <div>
    <UserNav />
    
    <main class="main">
      <br>
      <section class="book-grid">
        <article class="book" v-for="(book, index) in books" :key="book.id">
          <div class="book-content">
            <img :src="getImageUrl(book.image)" alt="No Image Available" @error="handleImageError">
            <div class="book-info">
              <h3>{{ book.title }}</h3>
              <p>by {{ book.author }}</p>
              <p>{{ book.section }}</p>
            </div>
          </div>  
          <div class="button">
            <button type="button" class="btn btn-outline-info" @click="borrowBook(book.id)">Borrow Book</button>
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
</script>

<style scoped>
body {
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f7f7f7;
}

.main {
  font-family: 'Roboto', sans-serif;
  padding: 20px;
  background-color: #f7f7f7;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 47px;
  margin-left: 20px;
  margin-right: 25px;
}

.book {
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.book:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.book img {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
}

.book-info {
  padding: 15px;
  text-align: center;
}

.book-info h3 {
  font-size: 20px;
  margin: 0 0 10px;
  color: #333;
}

.book-info p {
  margin: 5px 0;
  color: #777;
}

.button {
  margin-top: auto;
  width: 100%;
}

.button button {
  width: 100%;
  padding: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 0 0 10px 10px;
}

.button button:hover {
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
</style>
