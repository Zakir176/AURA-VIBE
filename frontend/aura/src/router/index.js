import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import SessionCreate from "@/views/SessionCreate.vue";

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/create", name: "CreateSession", component: SessionCreate },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
