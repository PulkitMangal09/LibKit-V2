<template>
<header class="navbar-header">
    <div class="container">

      <router-link to='/'  class="brand-logo">

        <h1 class="brand-name" style="font-family: Zapfino; font-style: italic; ">LibKit </h1>

    </router-link>
      <nav>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/register" class="nav-link">Register</router-link>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<style scoped>
 .navbar-header {
  background-color:#7FC7D9;
  padding: 19px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1280px;
  margin: 0 120px;
  padding: 0 0px;
  
}

.brand-logo {
  text-decoration: none;
}

.brand-name {
  /* font-family: 'Zapfino', sans-serif;
  font-style: italic; */
  color: #fff;
  text-decoration: none;
  font-size: 28px;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 20px;
}

.nav-item {
  display: inline;
}

.nav-link {
  text-decoration: none;
  color: #fff;
  font-weight: 600;
  padding: 10px 15px;
  transition: color 0.3s ease, background-color 0.3s ease;
}

.nav-link:hover {
  color: #fff;
  background-color: #0056b3;
  border-radius: 5px;
}
</style>