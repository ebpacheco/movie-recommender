// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user  = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email, password) {
    const { data } = await api.post('/auth/login', { email, password })

    token.value = data.access_token
    localStorage.setItem('token', data.access_token)

    try {
      await fetchUser()
    } catch {
      logout()
      throw new Error('Erro ao carregar usuário')
    }
  }

  async function register(payload) {
    await api.post('/auth/register', payload)
    await login(payload.email, payload.password)
  }

  async function fetchUser() {
    const { data } = await api.get('/users/me')
    user.value = data
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('token')

    // Limpa stores derivadas para evitar estado stale entre sessões
    import('@/stores/profile').then(({ useProfileStore }) => useProfileStore().clear())
    import('@/stores/recommendations').then(({ useRecommendationsStore }) => useRecommendationsStore().clear())
  }

  return { token, user, isAuthenticated, login, register, fetchUser, logout }
})
