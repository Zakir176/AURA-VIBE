import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  // {
  //   path: '/',
  //   name: 'Landing',
  //   component: () => import('@/views/LandingPage.vue')
  // },
  // {
  //   path: '/create',
  //   name: 'CreateSession',
  //   component: () => import('@/views/CreateSession.vue')
  // },
  // {
  //   path: '/join',
  //   name: 'JoinSession',
  //   component: () => import('@/views/JoinSession.vue')
  // },
  // {
  //   path: '/session/:sessionCode',
  //   name: 'SessionPage',
  //   component: () => import('@/views/SessionPage.vue'),
  //   props: true
  // }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router