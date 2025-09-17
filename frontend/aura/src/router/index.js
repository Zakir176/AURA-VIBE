import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import GetStarted from "@/views/GetStarted.vue";
import SessionCreate from "@/views/SessionCreate.vue";
import JoinSession from "@/views/JoinSession.vue";

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/get-started", name: "GetStarted", component: GetStarted },
  { path: "/create", name: "CreateSession", component: SessionCreate },
  { path: "/join", name: "JoinSession", component: JoinSession },
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

export default router;
