// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginView           from '@/views/LoginView.vue'
import RegisterView        from '@/views/RegisterView.vue'
import RecommendationsView from '@/views/RecommendationsView.vue'

const routes = [
  { path: '/',               redirect: '/recommendations' },
  { path: '/login',          component: LoginView },
  { path: '/register',       component: RegisterView },
  { path: '/recommendations', component: RecommendationsView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) return '/login'
})

export default router
