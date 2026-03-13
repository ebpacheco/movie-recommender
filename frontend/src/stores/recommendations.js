// src/stores/recommendations.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRecommendationsStore = defineStore('recommendations', () => {
  const movies          = ref([])
  const aiMessage       = ref('')
  const nextAvailableAt = ref(null)
  const cached          = ref(false)

  function set(data) {
    movies.value          = data.movies          ?? []
    aiMessage.value       = data.message         ?? ''
    nextAvailableAt.value = data.next_available_at ?? null
    cached.value          = data.cached           ?? false
  }

  function clear() {
    movies.value          = []
    aiMessage.value       = ''
    nextAvailableAt.value = null
    cached.value          = false
  }

  return { movies, aiMessage, nextAvailableAt, cached, set, clear }
})
