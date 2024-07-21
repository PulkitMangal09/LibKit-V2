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
      <div v-for="(item, index) in mainData" :key="index" class="box1 box">
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

    <!-- Rating Modal -->
    <RatingModal 
      :visible="isRatingModalVisible" 
      title="Rate the Book" 
      @confirm="submitRating" 
      @cancel="closeRatingModal" 
    />

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-if="noRequestError" class="noRequestError-message">
      {{ noRequestError }}
    </div>

  </div>
</template>

<script setup>
import MyBooksNav from '@/components/MyBooksNav.vue';
import ConfirmationModal from '@/components/ConfirmationModal.vue';
import RatingModal from '@/components/RatingModal.vue'; // Import the Rating Modal
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
// import { s } from 'vite/dist/node/types.d-aGj9QkWt';

const mainData = ref([]);
const error = ref('');
const router = useRouter();
const isModalVisible = ref(false);
const isRatingModalVisible = ref(false); // State for rating modal visibility
const bookToReturn = ref(null);
const bookIdForRating = ref(null); // Book ID to be used for submitting rating
const successMessage = ref('');
const errorMessage = ref('');
const noRequestError = ref('');
const rating = ref(0);
const selectedRating = ref(0); // State for selected rating

const fetchData = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://localhost:5000/user_approved_books', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    mainData.value = Object.values(response.data);
    if (Object.values(response.data).length === 0) {
      noRequestError.value = 'No books found';
    }
    else {
      noRequestError.value = '';
    }
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
  bookToReturn.value = id;
  isModalVisible.value = true;
};

const handleConfirm = async () => {
  if (bookToReturn.value !== null) {
    const response = await returnBook(bookToReturn.value);
    if (response) {
    bookIdForRating.value = response.data.book_id; // Set the book ID for rating
    isModalVisible.value = false;
    setTimeout(() => {
      isRatingModalVisible.value = true; // Show rating modal after a delay
    }, 2000);
  }
}
};

const handleCancel = () => {
  isModalVisible.value = false;
};

const closeRatingModal = () => {
  isRatingModalVisible.value = false;
};

const submitRating = async (rating) => {
  if (bookIdForRating.value !== null) {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`http://localhost:5000/api/feedback/${bookIdForRating.value}`, { 
        rating: rating
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      // console.log(rating);
      successMessage.value = 'Rating submitted successfully';
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } catch (err) {
      console.error('Error submitting rating:', err);
      errorMessage.value = 'An error occurred while submitting the rating';
      setTimeout(() => {
        errorMessage.value = '';
      }, 3000);
    }
    closeRatingModal();
  }
};

const returnBook = async (id) => {
  try {
    const token = localStorage.getItem('token');
    const response =await axios.get(`http://localhost:5000/return_book/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    successMessage.value = 'Book returned successfully';
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
    fetchData();
    return response; // Return the response to handle the book ID
  } catch (err) {
    console.error('Error returning the book:', err);
    errorMessage.value = 'An error occurred while returning the book';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
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
  .box1 {
    width: calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .box1 {
    width: 100%;
  }
}

.noRequestError-message {
  position: fixed;
  left: 50%;
  margin-top: 300px;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 1000;
  width: fit-content;
  font: 1em sans-serif;
}

</style>
