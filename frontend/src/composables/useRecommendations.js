// src/composables/useRecommendations.js
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRecommendationsStore } from '@/stores/recommendations'
import { useCountdown } from '@/composables/useCountdown'
import api from '@/services/api'
import { enrichMovies, useLocaleTranslation } from '@/composables/useMovieEnrich'

export function useRecommendations() {
  const { t, locale } = useI18n()
  const auth  = useAuthStore()
  const route = useRoute()
  const store = useRecommendationsStore()
  const { countdown, startCountdown } = useCountdown()

  const loading           = ref(false)
  const translating       = ref(false)
  const error             = ref('')
  const mood              = ref('')
  const movies            = ref([])
  const aiMessage         = ref('')
  const originalAiMessage = ref('')
  const originalAiLocale  = ref('')

  useLocaleTranslation(movies, translating, aiMessage, originalAiMessage, originalAiLocale)

  function setAiMessage(message, lang) {
    aiMessage.value         = message || ''
    originalAiMessage.value = message || ''
    originalAiLocale.value  = lang || locale.value
  }

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

  async function enrich(rawMovies) {
    return enrichMovies(rawMovies, locale.value, {
      watchRegion:     userCountry.value,
      userPlatformIds: userPlatforms.value.length ? userPlatforms.value : null,
    })
  }

  async function loadCached() {
    await auth.fetchUser()
    try {
      const { data } = await api.get('/recommendations/latest')
      movies.value = await enrich(data.movies)
      setAiMessage(data.message, data.language || locale.value)
      store.set(data)
      if (data.next_available_at) startCountdown(data.next_available_at)
    } catch {} // 404 = sem cache
  }

  async function generate() {
    loading.value = true
    error.value   = ''
    try {
      const baseURL = `${import.meta.env.VITE_API_URL ?? ''}/api/v1`
      const token   = localStorage.getItem('token')
      const res     = await fetch(`${baseURL}/recommendations/stream`, {
        method:  'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ mood: mood.value || null, language: locale.value }),
      })

      if (res.status === 401 && token) {
        localStorage.removeItem('token')
        window.location.href = '/login'
        return
      }
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || t('recommendations.error'))
      }

      const reader  = res.body.getReader()
      const decoder = new TextDecoder()
      let   buffer  = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
      }

      const MARKER = '\n__RESULT__\n'
      const idx    = buffer.indexOf(MARKER)
      if (idx === -1) throw new Error(t('recommendations.error'))

      const data = JSON.parse(buffer.slice(idx + MARKER.length).trim())
      movies.value = await enrich(data.movies)
      setAiMessage(data.message, locale.value)
      store.set(data)
      if (data.next_available_at) startCountdown(data.next_available_at)
    } catch (e) {
      error.value = e.message || t('recommendations.error')
    } finally {
      loading.value = false
    }
  }

  onMounted(loadCached)

  watch(() => route.path, (path) => {
    if (path === '/recommendations') auth.fetchUser()
  })

  return {
    loading, translating, error, mood, movies, aiMessage,
    countdown, isAdmin, hasRecommendation, isProfileComplete,
    userPlatforms, userGenres, userMovies,
    generate,
  }
}
