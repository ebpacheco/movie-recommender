// src/stores/streaming.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getAllProviders } from '@/services/tmdb'

export const useStreamingStore = defineStore('streaming', () => {
  const popular = ref([])
  const others  = ref([])
  const loaded  = ref(false)

  async function load() {
    if (loaded.value) return
    const result = await getAllProviders('BR', 'pt-BR')
    popular.value = result.popular
    others.value  = result.others
    loaded.value  = true
  }

  return { popular, others, loaded, load }
})
