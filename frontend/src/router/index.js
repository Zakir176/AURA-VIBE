import { createRouter, createWebHistory } from 'vue-router'

// Import views (pages) that will be displayed for each route
import Landing from '@/views/Landing.vue'
import CreateSession from '@/views/CreateSession.vue'
import JoinSession from '@/views/JoinSession.vue'
import QueueView from '@/views/QueueView.vue'

const routes = [
  // Route for the landing page
  {
    path: '/',
    name: 'Landing',
    component: Landing,
  },
  // Route for creating a session
  {
    path: '/create',
    name: 'CreateSession',
    component: CreateSession,
  },
  // Route for joining a session (via code or QR code)
  {
    path: '/join',
    name: 'JoinSession',
    component: JoinSession,
  },
  // Route for managing the queue (after joining a session)
  {
    path: '/session/:sessionCode',
    name: 'QueueView',
    component: QueueView,
    props: true, // This allows us to pass the sessionCode as a prop to the QueueView component
  },
]

// Create the router instance with the routes
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Use HTML5 History Mode
  routes,
})

export default router
