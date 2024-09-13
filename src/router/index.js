import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ViewBook from '../views/ViewBook.vue'
import MyBooks from '../views/MyBooks.vue'
import MainPage from '../views/Mainpage.vue'
import ReadReviews from '@/views/ReadReviews.vue'
import RegisterUser from '@/views/RegisterUser.vue'
import AdminLogin from '@/views/Admin/AdminLogin.vue'
import ManageCategory from  '@/views/Admin/ManageCategory.vue'
import AdminManageBooks from '../views/Admin/ManageBooks.vue'

import AdminMainpage from '../views/Admin/Mainpage.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/AdminManageBooks',
      name: 'AdminManageBooks',
      component:AdminManageBooks
    },
    {
      path: '/',
      name: 'MainPage',
      component: MainPage
    },


    {
      path: '/ManageCategory',
      name: 'ManageCategory',
      component: ManageCategory
    },
    
    

    {
      path: '/AdminMainpage',
      name: 'AdminMainpage',
      component: AdminMainpage
    },


    {
      path: '/RegisterUser',
      name: 'RegisterUser',
      component: RegisterUser
    },

    {
      path: '/AdminLogin',
      name: 'AdminLogin',
      component: AdminLogin
    },


    
    {
      path: '/StudentHome',
      name: 'home',
      component: HomeView,
      
      beforeEnter(to, from, next) {
        // Check if the user is authenticated (i.e., token exists)
        const token = localStorage.getItem('token');
        if (token) {
          // User is authenticated, allow access to the route
          next();
        } else {
          // User is not authenticated, redirect to login page
          next('/');
        }
      }
    },
    {
      path: '/StudentBooks',
      name: 'StudentBooks',
      component: MyBooks
    },


    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    
    {
      path: '/StudentHome',
      name: 'StudentHome',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/StudentHome.vue')
    },

    
    {
      path: '/view-book/:bookId', // Assuming bookId is passed as a route parameter
      name: 'view-book',
      component: ViewBook
    }, 
    
    {
      path: '/ReadReviews/:bookId',
      name: 'ReadReviews',
      component: ReadReviews
    },


  ]
})

export default router
