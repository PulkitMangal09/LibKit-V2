<template>
    <header>
      <nav class="navbar navbar-default" style="background-color: #7FC7D9; padding: 0px;">
        <div class="container-fluid">
          <div class="navbar-header">
            <router-link class="navbar-brand" :to="{ name: 'AdminDash' }" style="font-size: 28px; margin-left: 30px;">
              <span style="font-family: Zapfino; font-style: italic; color: white"><strong>LibKit</strong></span>
            </router-link>
          </div>
          <div class="container-fluid col-md-3" style="margin-left: 300px;">
            <form class="d-flex" role="search" @submit.prevent="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
              <button type="submit">Filter</button>
            </form>
          </div>
          <ul class="nav navbar-nav navbar-right">
            <li>
              <div class="btn-group">
                <button class="btn btn-outline  navbar-btn" @click="navigateTo('AdminDash')" style=" border-radius: 5px; ">Home</button>
                <button class="btn btn-outline navbar-btn" @click="navigateTo('Requests')" style="border-radius: 5px; background-color: #3887BE; margin-right: 30px; color: white">Requests</button>
                <button class="btn btn-outline navbar-btn" @click="navigateTo('GeneralStats')" style="border-radius: 5px;">Stats</button>
                <button class="btn btn-outline navbar-btn" @click="logout" style="border-radius: 5px;">Logout</button>
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
      },
      logout () {
        localStorage.removeItem('token');
        this.$router.push({ name: 'login' });
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
  </style>
  