<template>
        <div class="slide" >
            <img src="@/assets/BP_slide.png" alt="Book Cover" />
            <div class="slide-content">
              <h2 class="book-title"> BLACKPINK - Rolling Stone Magazine </h2>
              <p class="book-author">by BLACKPINK</p>
              <div class="rating">
                <span v-for="star in getStarRating(5)" :key="star" class="star">★</span>
              </div>
              <p class="hot-book">Trending on LibKit</p>
            </div>
        </div>
  </template>


<!-- v-for="(book, index) in top_books" :key="index" class="slide" v-show="currentIndex === index" -->
  
  <script setup>
  // import { ref, onMounted } from 'vue';
  // // import axios from 'axios';
  // import { useRouter } from 'vue-router';
  
  // const top_books = ref([]);
  // const currentIndex = ref(0);
  // const router = useRouter();
    
  // const handleImageError = (event) => {
  //   event.target.src = 'http://localhost:5000/static/images/default.jpg';
  // };
  
  const getStarRating = (rating) => {
    return Array.from({ length: Math.round(rating) }, (_, i) => i);
  };
  
  //const topBooks = async () => {
   // try {
   //   const token = localStorage.getItem('token');
    //  const response = await axios.get('http://localhost:5000/top_books', {
   //     headers: {
   //       Authorization: `Bearer ${token}`
   //     }
   //   });
   //   top_books.value = response.data;
   // } catch (error) {
   //   if (error.response && error.response.status === 401) {
   //     router.push({ name: 'login' });
   //   } else {
    //    console.error(error);
    //  }
  //  }
 // };
  
 // onMounted(() => {
   // topBooks();
 // });
  </script>
  
  <style scoped>
  .slide {
    min-width: 80%;
    box-sizing: border-box;
    height: 80%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-top: 20px;
  }
  
  img {
    width: 95vw;
    height: 500px;
    object-fit: cover;
    border-radius: 10px;
  }
  
  .slide-content {
    position: absolute;
    bottom: 0;
    /* left: 30px; */
    background-color: rgba(0, 0, 0, 0.6);
    padding: 20px;
    border-radius: 10px;
    color: #fff;
    width: calc(95% - -30px);
    text-align: center;
  }
  
  .book-title {
    font-size: 2rem;
    margin-bottom: 10px;
    animation: glow 1s ease-in-out infinite alternate;
  }
  
  .book-author {
    font-size: 1.2rem;
    margin-bottom: 10px;
  }
  
  .rating .star {
    color: gold;
    font-size: 1.5rem;
  }
  
  .hot-book {
    font-size: 1rem;
    
    
  }

  @keyframes glow {
    from {
      text-shadow: 0 0 10px #fff, 0 0 20px #ff6347, 0 0 30px #ff6347, 0 0 40px #ff6347;
    }
    to {
      text-shadow: 0 0 20px #fff, 0 0 30px #ff6347, 0 0 40px #ff6347, 0 0 50px #ff6347;
    }
  }

  </style>
  