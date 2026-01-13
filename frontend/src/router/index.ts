import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('@/views/LandingPage.vue'),
    meta: { hideHeader: true }
  },
  {
    path: '/create',
    name: 'CreateSession',
    component: () => import('@/views/CreateSession.vue')
  },
  {
    path: '/join',
    name: 'JoinSession',
    component: () => import('@/views/JoinSession.vue')
  },
  {
    path: '/session/:sessionCode',
    name: 'SessionPage',
    component: () => import('@/views/SessionPage.vue'),
    props: true,
    meta: { hideHeader: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/sessions',
    name: 'Sessions',
    component: () => import('@/views/Sessions.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
