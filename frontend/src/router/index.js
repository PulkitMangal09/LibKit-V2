import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDash  from '@/views/AdminDash.vue'
import AddSection from '@/views/AddSection.vue'
import SectionView from '@/views/SectionView.vue'
import UpdateSection from '@/views/UpdateSection.vue'
import AddBook from '@/views/AddBook.vue'
import UpdateBook from '@/views/UpdateBook.vue'
import UserDash from '@/views/UserDash.vue'
import MyBooks from '@/views/MyBooks.vue'
import Requests from '@/views/Requests.vue'
import UserApprovedView from '@/views/UserApprovedView.vue'
import AdminApprovedBooks from '@/views/AdminApprovedBooks.vue'
import AdminRejectedView from '@/views/AdminRejectedView.vue'
import SearchView from '@/views/SearchView.vue'
import GeneralStats from '@/views/GeneralStats.vue'

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
    },

    {
      path: '/add_book/:id',
      name: 'AddBook',
      component: AddBook
    },

    {
      path: '/update_book/:id',
      name: 'UpdateBook',
      component: UpdateBook
    },

    // User Dashboard Starts

    {
      path: '/user_dash',
      name: 'UserDash',
      component: UserDash
    },

    // book cycle starts

    {
      path: '/my_books',
      name: 'MyBooks',
      component: MyBooks
    },

    // admin side view
    {
      path: '/requests',
      name: 'Requests',
      component: Requests
    },

    // User Approved View
    {
      path: '/user_approved_books',
      name: 'UserApprovedView',
      component: UserApprovedView

    },

    // admin approved view
    {
      path: '/admin_approved_books',
      name : 'AdminApprovedBooks',
      component: AdminApprovedBooks
    },

    // admin rejected view
    {
      path: '/admin_rejected_books',
      name : 'AdminRejectedView',
      component: AdminRejectedView
    },

    // search view
    {
      path: '/search',
      name : 'SearchView',
      component: SearchView
    },

    // general stats
    {
      path: '/stats',
      name : 'GeneralStats',
      component: GeneralStats
    },


  ]
})

export default router
