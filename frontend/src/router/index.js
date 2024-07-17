import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDash  from '@/views/AdminDash.vue'
import AddSection from '@/views/AddSection.vue'
import SectionView from '@/views/SectionView.vue'
import UpdateSection from '@/views/UpdateSection.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
      
    { path: '/register', 
      name: 'register', 
      component: RegisterView 
    },

    {
      path: '/admin_dash',
      name: 'AdminDash',
      component: AdminDash
    },

    {
      path: '/add_section',
      name: 'AddSection',
      component: AddSection
    },

    {
      path: '/section_view/:id',
      name: 'SectionView',
      component: SectionView
    },

    {
      path: '/update_section/:id',
      name: 'UpdateSection',
      component: UpdateSection
    }


  ]
})

export default router