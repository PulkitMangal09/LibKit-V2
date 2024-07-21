<template>
    <header>
      <nav class="navbar navbar-default" style="background-color: #7FC7D9; padding: 0px;">
        <div class="container-fluid">
          <div class="navbar-header">
            <router-link class="navbar-brand" :to="{ name: 'UserDash' }" style="font-size: 28px; margin-left: 30px;">
              <span style="font-family: Zapfino; font-style: italic; color: white"><strong>LibKit</strong></span>
            </router-link>
          </div>
          <div class="container-fluid col-md-3" style="margin-left: 300px;">
    <div class="search-container">
      <input
        class="form-control me-2"
        type="search"
        placeholder="Search"
        aria-label="Search"
        v-model="searchQuery"
      />
      <button class="searchButton" type="submit">
        <img src="@/assets/searchImage.png" alt="Search" />
      </button>
    </div>
  </div>
          <ul class="nav navbar-nav navbar-right">
            <li>
              <div class="btn-group">
                <button class="btn navbar-btn" @click="navigateTo('UserDash')" style="background-color: #3887BE; margin-right: 30px; border-radius: 5px; color: white">All Books</button>
                <button class="btn btn-outline navbar-btn" @click="navigateTo('MyBooks')" style="border-radius: 5px;">My Books</button>
                <button class="btn btn-outline navbar-btn" @click="navigateTo('GeneralStats')" style="border-radius: 5px;">Stats</button>
                <button class="btn btn-outline navbar-btn" @click="navigateTo('login')" style="border-radius: 5px;">Logout</button>
              </div>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: ''
      };
    },
    methods: {
      navigateTo(routeName) {
        this.$router.push({ name: routeName });
      },
      search() {
        console.log('Searching for:', this.searchQuery);
      }
    }
  };
  </script>
  

  <style scoped>

  .btn-outline {
    background-color: transparent;
    color: white;
    border: 1px solid #7FC7D9;
    margin-right: 30px;
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
  width: 20px; /* Adjust size as needed */
  height: 16px; /* Adjust size as needed */
}
  </style>
  