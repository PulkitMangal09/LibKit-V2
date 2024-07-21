<template>
    <div v-if="visible" class="modal-overlay">
      <div class="modal-container">
        <h3>{{ title }}</h3>
        <div class="rating-container">
          <span 
            v-for="star in 5" 
            :key="star" 
            :class="['star', { 'selected': star <= selectedRating }]" 
            @click="selectRating(star)"
          >
            ★
          </span>
        </div>
        <div class="modal-buttons">
          <button class="btn btn-primary" @click="confirmRating">Submit</button>
          <button class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue';
  
  const props = defineProps({
    visible: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      required: true
    }
  });
  
  const emit = defineEmits(['confirm', 'cancel']);
  
  const selectedRating = ref(0);
  
//   watch(() => props.visible, (newVal) => {
//     if (!newVal) {
//       selectedRating.value = 0;
//     }
//   });
  
  const selectRating = (rating) => {
    selectedRating.value = rating;
  };
  
  const confirmRating = () => {
    emit('confirm', selectedRating.value);
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
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
  }
  
  .rating-container {
    margin: 20px 0;
  }
  
  .star {
    font-size: 2rem;
    color: #ccc;
    cursor: pointer;
  }
  
  .star.selected {
    color: #f5c518;
  }
  
  .modal-buttons {
    display: flex;
    justify-content: space-around;
    
  }

  .btn {
    margin-right: 15px;
    margin-left: 10px;
  }
  </style>
  