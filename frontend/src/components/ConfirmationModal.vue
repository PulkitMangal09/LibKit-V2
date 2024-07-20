<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal">
      <h3>{{ title }}</h3>
      <p>{{ message }}</p>
      <div class="modal-buttons">
        <button @click="confirm">Yes</button>
        <button @click="cancel">No</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  visible: Boolean,
  title: String,
  message: String
});

const emit = defineEmits(['confirm', 'cancel']);

const confirm = () => {
  emit('confirm');
};

const cancel = () => {
  emit('cancel');
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

.modal {
  position: relative; /* Ensure it is positioned within the overlay */
  background: white;
  padding: 20px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 350px; /* Adjust width as needed */
  z-index: 10000; /* Ensure it is on top of everything */
  display: block; /* Ensure it is displayed */
}


.modal-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.modal-buttons button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-buttons button:first-child {
  background-color: #007bff;
  color: white;
}

.modal-buttons button:last-child {
  background-color: #6c757d;
  color: white;
}
</style>
