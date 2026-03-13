// src/stores/profile.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref(null)
  const loaded  = ref(false)

  async function fetch() {
    const { data } = await api.get('/users/me/profile')
    profile.value = data
    loaded.value  = true
  }

  function patch(updates) {
    if (profile.value) Object.assign(profile.value, updates)
  }

  function clear() {
    profile.value = null
    loaded.value  = false
  }

  return { profile, loaded, fetch, patch, clear }
})
