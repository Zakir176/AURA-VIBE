import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/pages/LandingPage.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage,
  },
  // Add other routes here later
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
