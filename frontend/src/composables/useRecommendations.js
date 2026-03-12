// src/composables/useRecommendations.js
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { enrichMovies, useLocaleTranslation } from '@/composables/useMovieEnrich'

export function useRecommendations() {
  const { t, locale } = useI18n()
  const auth  = useAuthStore()
  const route = useRoute()

  const loading         = ref(false)
  const translating     = ref(false)
  const error           = ref('')
  const mood            = ref('')
  const movies          = ref([])
  const aiMessage       = ref('')
  const nextAvailableAt = ref(null)
  const countdown       = ref('')
  let   countdownTimer  = null

  useLocaleTranslation(movies, translating)

  const userCountry       = computed(() => auth.user?.profile?.country || 'BR')
  const userPlatforms     = computed(() => auth.user?.profile?.streaming_platforms || [])
  const userGenres        = computed(() => auth.user?.profile?.favorite_genres || [])
  const userMovies        = computed(() => auth.user?.profile?.favorite_movies || [])
  const isAdmin           = computed(() => auth.user?.role === 'admin')
  const hasRecommendation = computed(() => movies.value.length > 0)
  const isProfileComplete = computed(() =>
    userPlatforms.value.length >= 1 &&
    userGenres.value.length   >= 3
  )

  // ── Countdown ───────────────────────────────────────────────────────────────

  function startCountdown(nextAt) {
    nextAvailableAt.value = new Date(nextAt)
    if (countdownTimer) clearInterval(countdownTimer)

    function tick() {
      const diff = nextAvailableAt.value - Date.now()
      if (diff <= 0) {
        countdown.value       = ''
        nextAvailableAt.value = null
        clearInterval(countdownTimer)
        return
      }
      const h   = Math.floor(diff / 3_600_000)
      const min = Math.floor((diff % 3_600_000) / 60_000)
      countdown.value = h > 0 ? `${h}h ${min}min` : `${min}min`
    }

    tick()
    countdownTimer = setInterval(tick, 30_000)
  }

  function clearCountdown() {
    if (countdownTimer) clearInterval(countdownTimer)
  }

  // ── Enrich ──────────────────────────────────────────────────────────────────

  async function enrich(rawMovies) {
    return enrichMovies(rawMovies, locale.value, {
      watchRegion:     userCountry.value,
      userPlatformIds: userPlatforms.value.length ? userPlatforms.value : null,
    })
  }

  // ── API ─────────────────────────────────────────────────────────────────────

  async function loadCached() {
    // Sempre re-busca para pegar preferências atualizadas
    await auth.fetchUser()
    try {
      const { data } = await api.get('/recommendations/today')
      movies.value    = await enrich(data.movies)
      aiMessage.value = data.message || ''
      if (data.next_available_at) startCountdown(data.next_available_at)
    } catch {} // 404 = sem cache
  }

  async function generate() {
    loading.value = true
    error.value   = ''
    try {
      const { data } = await api.post('/recommendations', {
        mood:     mood.value || null,
        language: locale.value,
      })
      movies.value    = await enrich(data.movies)
      aiMessage.value = data.message || ''
      if (data.next_available_at) startCountdown(data.next_available_at)
    } catch (e) {
      error.value = e.response?.data?.detail || t('recommendations.error')
    } finally {
      loading.value = false
    }
  }

  onMounted(loadCached)

  // Re-busca usuário sempre que navegar de volta para esta página
  watch(() => route.path, (path) => {
    if (path === '/recommendations') auth.fetchUser()
  })
  onUnmounted(clearCountdown)

  return {
    loading, translating, error, mood, movies, aiMessage,
    countdown, isAdmin, hasRecommendation, isProfileComplete,
    userPlatforms, userGenres, userMovies,
    generate,
  }
}