// src/composables/useCountdown.js
import { ref, onUnmounted } from 'vue'

export function useCountdown() {
  const countdown       = ref('')
  const nextAvailableAt = ref(null)
  let   timer           = null

  function tick() {
    if (!nextAvailableAt.value) return
    const diff = nextAvailableAt.value - Date.now()
    if (diff <= 0) {
      countdown.value       = ''
      nextAvailableAt.value = null
      clearInterval(timer)
      timer = null
      return
    }
    const h   = Math.floor(diff / 3_600_000)
    const min = Math.floor((diff % 3_600_000) / 60_000)
    countdown.value = h > 0 ? `${h}h ${min}min` : `${min}min`
  }

  function startCountdown(nextAt) {
    const utc = typeof nextAt === 'string' && !nextAt.endsWith('Z') && !nextAt.includes('+')
      ? nextAt + 'Z'
      : nextAt
    nextAvailableAt.value = new Date(utc)
    if (timer) clearInterval(timer)
    tick()
    timer = setInterval(tick, 30_000)
  }

  function clearCountdown() {
    if (timer) clearInterval(timer)
    timer = null
  }

  onUnmounted(clearCountdown)

  return { countdown, nextAvailableAt, startCountdown, clearCountdown }
}
