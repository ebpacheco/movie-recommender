// src/composables/useRecommendationLock.js
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useCountdown } from '@/composables/useCountdown'

export function useRecommendationLock() {
  const isLocked = ref(false)
  const { countdown, nextAvailableAt, startCountdown } = useCountdown()

  async function checkLock() {
    try {
      const { data } = await api.get('/recommendations/latest')
      if (data.next_available_at) {
        startCountdown(data.next_available_at)
        isLocked.value = nextAvailableAt.value > new Date()
      }
    } catch {} // 404 = sem recomendação ativa
  }

  onMounted(checkLock)

  return { isLocked, countdown }
}
