<template>
    <div v-if="visible" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h5>{{ book?.title }}</h5>
          <button @click="closeModal" class="closeModal">Close</button>
        </div>
        <div class="modal-body">
          <div class="modal-content">
            <div class="modal-image">
              <img :src="getImageUrl(book?.image)" alt="Book Cover" @error="handleImageError" />
              <p><strong>Author:</strong> {{ book?.author }}</p>
            </div>
            <div class="modal-details">
              <p class="content" ><strong>Content:</strong> {{ book?.content }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { ref, watch, computed } from 'vue';
  import { defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    visible: {
      type: Boolean,
      required: true
    },
    book: {
      type: Object,
      default: () => ({})
    }
  });
  
  const emit = defineEmits(['close']);
  
  const closeModal = () => {
    emit('close');
  };
  
  const getImageUrl = (image) => {
    return image ? `http://localhost:5000/static/images/${image}` : 'http://localhost:5000/static/images/default.jpg';
  };
  
  const handleImageError = (event) => {
    event.target.src = 'http://localhost:5000/static/images/default.jpg';
  };
  </script>
  
  <style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 600px; /* Adjust width as needed */
  max-width: 90%;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  margin-top: 10px;
  display: flex;
}

.modal-content {
  display: flex;
  width: 100%;
  flex-direction: row;
}

.modal-image {
  width: 30%;
  padding-right: 20px;
  margin-left: 15px;
  margin-top: 15px;
}

.modal-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 10px;
}

.modal-details {
  width: 70%;
}

.modal-details p {
  margin: 5px 0;
}

.closeModal {
  background: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.content{
    white-space: pre-wrap;
    color: black;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    margin: 0;
    padding: 0;
    text-align: left;
    text-decoration: none;
    text-transform: none;
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin-top: 15px;
    margin-bottom: 15px;
    padding: 0 20px;
}

</style>
