import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import GetStarted from "@/views/GetStarted.vue";
import SessionCreate from "@/views/SessionCreate.vue";
import JoinSession from "@/views/JoinSession.vue";
import Login from "@/views/Login.vue";
import Landing from "@/views/Landing.vue";
import Session from "@/views/Session.vue";
import { isAuthenticated } from "@/utils/auth.js";
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const routes = [
  { path: "/login", name: "Login", component: Login },
  // Callback handled by backend; no client route needed

  { path: "/", name: "Home", component: Home },
  { path: "/get-started", name: "GetStarted", component: GetStarted, meta: { requiresAuth: true } },
  { path: "/create", name: "CreateSession", component: SessionCreate, meta: { requiresAuth: true } },
  { path: "/join", name: "JoinSession", component: JoinSession, meta: { requiresAuth: true } },
  { path: "/landing", name: "Landing", component: Landing },
  { path: "/session", name: "Session", component: Session },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    return { top: 0, behavior: 'smooth' }
  }
});

router.beforeEach(async (to, from, next) => {
  if (to.meta && to.meta.requiresAuth) {
    try {
      const res = await fetch(`${API_BASE}/api/auth/session`, { credentials: 'include' })
      const data = await res.json()
      if (data && data.authenticated) {
        next()
        return
      }
    } catch (e) {}
    const redirect = encodeURIComponent(to.fullPath || '/')
    next({ name: 'Login', query: { redirect } })
  } else {
    next()
  }
})

export default router;
