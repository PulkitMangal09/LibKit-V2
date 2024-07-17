<template>
    <div>
      <header>
        <div class="container">
          <a href="#" @click.prevent="reloadPage"><h1><span style="font-family: Zapfino; font-style: italic;">LibKit</span></h1></a>
          <nav>
            <ul>
              <li><a href="#features" @click.prevent="scrollToSection('features')">Features</a></li>
              <li><a href="#about" @click.prevent="scrollToSection('about')">About</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </nav>
        </div>
      </header>
  
      <section id="hero">
        <div class="container">
          <h2>Manage Your Library Effortlessly with <span style="font-family: Zapfino; font-style: italic;">LibKit</span></h2>
          <p>A comprehensive solution to organize, track, and manage your library resources efficiently.</p>
          <router-link to='/login' class="btn">Get Started</router-link>
        </div>
      </section>
  
      <section id="features">
        <div class="container">
          <h2>Key Features</h2>
          <div class="feature">
            <h3>Book Management</h3>
            <p>Efficiently manage your book catalog with advanced search and categorization options.</p>
          </div>
          <div class="feature">
            <h3>User Management</h3>
            <p>Manage user accounts, issue books, and track borrowing history seamlessly.</p>
          </div>
        </div>
      </section>
  
      <section id="about">
        <div class="container">
          <h2>About LibKit</h2>
          <p>LibKit is a library management application developed by Pulkit. It aims to streamline library operations and improve user experience for both librarians and patrons.</p>
        </div>
      </section>
  
      <footer id="contact">
        <div class="container">
          <p>Connect with us:</p>
          <ul class="social-icons">
            <li><a href="https://www.instagram.com/pulkitmangal09?utm_source=qr&igshid=MTU2Mmdxd2x1YjZoNw=="><img src="https://w7.pngwing.com/pngs/722/1011/png-transparent-logo-icon-instagram-logo-instagram-logo-purple-violet-text-thumbnail.png" alt="Instagram"></a></li>
            <li><a href="#"><img src="https://freelogopng.com/images/all_img/1690643591twitter-x-logo-png.png" alt="Twitter"></a></li>
            <li><a href="https://www.linkedin.com/in/pulkit-mangal-09ab09257?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/480px-LinkedIn_logo_initials.png" alt="LinkedIn"></a></li>
          </ul>
          <p>&copy; 2024 LibKit by Pulkit. All rights reserved.</p>
        </div>
      </footer>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  
  const reloadPage = () => {
    location.reload()
  }
  
  const scrollToSection = (sectionId) => {
    const targetSection = document.getElementById(sectionId)
    if (targetSection) {
      targetSection.scrollIntoView({ behavior: 'smooth' })
    }
  }
  </script>
  
  <style>
  /* Reset CSS */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  /* Global Styles */
  body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  /* Header Styles */
  header {
    background-color: #7FC7D9;
    color: #fff;
    padding: 19px 0;
  }
  
  header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-left: 100px;
  }
  
  header h1 {
    font-size: 28px;
  }
  
  nav ul {
    list-style: none;
  }
  
  nav ul li {
    display: inline;
    margin-right: 20px;
  }
  
  nav ul li a {
    color: #fff;
    text-decoration: none;
  }
  
  /* Hero Section Styles */
  #hero {
    background-color: #f4f4f4;
    padding: 100px 0;
    text-align: center;
  }
  
  #hero h2 {
    font-size: 36px;
    margin-bottom: 20px;
  }
  
  #hero p {
    font-size: 18px;
    margin-bottom: 40px;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 20px;
    background-color: #333;
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
  }
  
  .btn:hover {
    background-color: #555;
  }
  
  /* Features Section Styles */
  #features {
    padding: 80px 0;
    text-align: center;
  }
  
  .feature {
    margin-bottom: 40px;
  }
  
  .feature h3 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  /* Footer Styles */
  footer {
    background-color: #333;
    color: #fff;
    padding: 40px 0;
    text-align: center;
  }
  
  .social-icons {
    margin-top: 20px;
  }
  
  .social-icons li {
    display: inline-block;
    margin-right: 10px;
  }
  
  .social-icons li img {
    width: 30px;
    height: auto;
  }
  
  .container a {
    color: #fff;
    text-decoration: none;
  }
  </style>
  