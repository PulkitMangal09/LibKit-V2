<template>
  <header>
    <nav class="navbar navbar-default" style="background-color: #7FC7D9; padding: 0px; height: 60px;">
      <div class="container-fluid">
        <div class="navbar-header">
          <router-link class="navbar-brand" :to="{ name: 'UserDash' }" style="font-size: 28px; margin-left: 30px;">
            <span style="font-family: Zapfino; font-style: italic; color: white"><strong>LibKit</strong></span>
          </router-link>
        </div>
        <div class="container-fluid col-md-3" style="margin-left: 200px;">
          <div class="search-container" >
            <input
              class="form-control me-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
              v-model="searchQuery"
              style="height: 40px;"
            />
            <button class="searchButton" @click="fetchResults">
              <img src="@/assets/searchImage.png" alt="Search" />
            </button>
          </div>
        </div>
        <ul class="nav navbar-nav navbar-right">
          <li>
            <div class="btn-group">
              <button class="btn navbar-btn" @click="navigateTo('UserDash')" style="background-color: #3887BE; margin-right: 30px; border-radius: 5px; color: white; height: 50px;">All Books</button>
              <button class="btn btn-outline navbar-btn" @click="navigateTo('MyBooks')" style="border-radius: 5px; height: 50px; ">My Books</button>
                
              
              <!-- Profile Dropdown -->
              <div class="btn-group profile-dropdown" @mouseover="showDropdown" @mouseleave="hideDropdown">
                <button class="btn btn-outline navbar-btn profile-btn"style="border-radius: 5px; ">
                  <img src="@/assets/pfp.jpg" alt="Profile" class="profile-image"/>
                  <p class="username">{{ username }} </p>
                </button>
                <div v-if="dropdownVisible" class="dropdown-menu dropdown-menu-right">
                  <!-- <button class="dropdown-item" @click="navigateTo('UserProfile')"> {{ username }} </button> -->
                  <button class="dropdown-item" @click="logout">Logout</button>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const searchQuery = ref('');
const router = useRouter();

const username = localStorage.getItem('username') || 'User';


const dropdownVisible = ref(false);

const showDropdown = () => {
  dropdownVisible.value = true;
};

const hideDropdown = () => {
  dropdownVisible.value = false;
};


const navigateTo = (routeName) => {
  router.push({ name: routeName });
};




const fetchResults = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get(`http://localhost:5000/search`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: {
        search: searchQuery.value
      }
    });
    
    router.push({ name: 'SearchView', query: { search: searchQuery.value } });

  } catch (error) {
    console.error(error);
    router.push({ name: 'UAView' });
  }
};


const logout = () => {
  localStorage.removeItem('token');
  router.push({ name: 'login' });
};

</script>

<style scoped>
.btn-outline {
  background-color: transparent;
  color: white;
  border: 1px solid #7FC7D9;
  margin-right: 30px;
  display: flex;
  align-items: center;
  height: 50px;
}

.btn-outline:hover {
  background-color: #3887BE;
  color: #fff;
}

.search-container {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;
}

.search-container input {
  flex: 1;
  border: none;
  padding: 10px;
  border-radius: 4px 0 0 4px;
  width: 300px;
}

.search-container button {
  background-color: #ffb84d; /* Orange background */
  border: none;
  padding: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 4px 4px 0;
}

.search-container button img {
  width: 22px; 
  height: 20px; 
}

.profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  vertical-align: middle;
}



.username {
  color: white;
  margin-left: 10px;
  margin-top: auto;
  font-size: 17px;
}

.profile-dropdown .dropdown-menu {
  display: block;
  position: absolute;
  top: 100%;
  left: 1;
  z-index: 1000;
  float: left;
  min-width: 10rem;
  padding: 0.5rem 0;
  margin: 0.125rem 0 0;
  font-size: 1rem;
  color: #212529;
  text-align: left;
  list-style: none;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid rgba(0,0,0,.15);
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,.175);
}

.navbar{
  min-height: 60px;
}

.dropdown-item:hover{
  color: black;
  background-color: #e71d36;
}

</style>
