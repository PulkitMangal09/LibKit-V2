<template>
  <div>
    <MyBooksNav />

    <ul class="nav nav-tabs justify-content-center mt-4">
      <li class="nav-item">
        <router-link :to="{ name: 'MyBooks' }" class="nav-link" active-class="active">Requests</router-link>
      </li>
      <li class="nav-item">
        <router-link :to="{ name: 'UserApprovedView' }" class="nav-link" active-class="active">Approved Books</router-link>
      </li>
    </ul>

    <div class="shop-section">
      <div v-for="(item, index) in mainData" :key="index" class="box1 box" >
        <div class="box-content">
          <div class="image-container">
            <img 
              :src="getImageUrl(item.image)" 
              alt="No Image Available" 
              @error="handleImageError"
            >
          </div>
          <div class="text-container">
            <h4>{{ item.title }}</h4>
            <p>Author: {{ item.author }}</p>
            <p>Content: 
                  <a :href="item.content" target="_blank">
                        {{ item.content }}
                    </a>
                </p>
          </div>
          <div class="button-container">
            <button 
              type="button" 
              class="btn btn-outline-warning" 
              @click="showModal(item.id)"
            >
              Return Book
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <ConfirmationModal 
      :visible="isModalVisible" 
      title="Confirm Return" 
      message="Are you sure you want to return this book?" 
      @confirm="handleConfirm" 
      @cancel="handleCancel" 
    />

  </div>
</template>

<script setup>
import MyBooksNav from '@/components/MyBooksNav.vue';
import ConfirmationModal from '@/components/ConfirmationModal.vue';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const mainData = ref([]);
const error = ref('');
const router = useRouter();
const isModalVisible = ref(false);
const bookToReturn = ref(null);

const fetchData = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://localhost:5000/user_approved_books', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    mainData.value = Object.values(response.data);
  } catch (err) {
    if (err.response && err.response.status === 401) {
      router.push({ name: 'login' });
    } else {
      error.value = 'An error occurred while fetching data';
      console.error(err);
    }
  }
};

const getImageUrl = (image) => `http://localhost:5000/static/images/${image}`;

const handleImageError = (event) => {
  event.target.src = 'http://localhost:5000/static/images/default.jpg';
};

const showModal = (id) => {
  console.log("Showing modal for book ID:", id);
  bookToReturn.value = id;
  isModalVisible.value = true;
};

const handleConfirm = async () => {
  if (bookToReturn.value !== null) {
    await returnBook(bookToReturn.value);
    isModalVisible.value = false;
  }
};

const handleCancel = () => {
  isModalVisible.value = false;
};

const returnBook = async (id) => {
  try {
    const token = localStorage.getItem('token');
    await axios.get(`http://localhost:5000/return_book/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    alert('Book returned successfully');
    fetchData();
  } catch (err) {
    console.error('Error returning the book:', err);
    alert('An error occurred while returning the book');
  }
};


onMounted(fetchData);
</script>

<style scoped>
.shop-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  justify-content: center;
}

.box1 {
  width: calc(33.333% - 60px);
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Ensure content is spaced */
  min-height: 450px; /* Ensure consistent card height */
}

.box1:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.box-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  flex: 1; /* Ensure the box-content takes up available space */
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

.button-container {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin-top: auto; /* Pushes the button to the bottom */
}

.btn {
  padding: 10px 20px;
  font-size: 0.875rem;
}

.nav-link.active {
  color: #495057;
  background-color: #e9ecef;
  border-color: #dee2e6 #dee2e6 #fff;
}

@media (max-width: 768px) {
  .box1 {
    width: calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .box1 {
    width: 100%;
  }
}
</style>
