import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginView            from '@/views/LoginView.vue'
import RegisterView         from '@/views/RegisterView.vue'
import RecommendationsView  from '@/views/RecommendationsView.vue'
import ProfileView          from '@/views/ProfileView.vue'
import UserPreferencesView  from '@/views/UserPreferencesView.vue'
import AdminView            from '@/views/AdminView.vue'
import AccountView          from '@/views/AccountView.vue'
import ForgotPasswordView   from '@/views/ForgotPasswordView.vue'
import ResetPasswordView    from '@/views/ResetPasswordView.vue'
import VerifyEmailView      from '@/views/VerifyEmailView.vue'

const routes = [
  { path: '/',                   redirect: '/recommendations' },
  { path: '/login',              component: LoginView,           meta: { public: true } },
  { path: '/register',           component: RegisterView,        meta: { public: true } },
  { path: '/forgot-password',    component: ForgotPasswordView,  meta: { public: true } },
  { path: '/reset-password',     component: ResetPasswordView,   meta: { public: true } },
  { path: '/verify-email',       component: VerifyEmailView,     meta: { standalone: true } },
  { path: '/recommendations',    component: RecommendationsView, meta: { requiresAuth: true } },
  { path: '/profile',            component: ProfileView,         meta: { requiresAuth: true } },
  { path: '/user-preferences',   component: UserPreferencesView, meta: { requiresAuth: true } },
  { path: '/admin',              component: AdminView,           meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/account',            component: AccountView,         meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, _from, next) => {
  const auth = useAuthStore()

  if (to.meta.standalone) return next()
  if (to.meta.requiresAuth && !auth.isAuthenticated) return next('/login')
  if (to.meta.public && auth.isAuthenticated) return next('/recommendations')

  if (to.meta.requiresAdmin) {
    if (!auth.user) await auth.fetchUser()
    if (auth.user?.role !== 'admin') return next('/recommendations')
  }

  next()
})

export default router