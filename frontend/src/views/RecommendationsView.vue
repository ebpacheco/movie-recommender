<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <!-- Hero -->
      <div class="hero">
        <div class="hero-text">
          <h1>{{ t('recommendations.hello') }} <span class="gold">{{ auth.user?.name?.split(' ')[0] }}</span> 👋</h1>
          <p>{{ t('recommendations.subtitle') }}</p>
        </div>
      </div>

      <!-- Prompt -->
      <div class="prompt-card">
        <label class="prompt-label">{{ t('recommendations.moodLabel') }}</label>
        <div class="prompt-row">
          <input
            v-model="mood"
            type="text"
            :placeholder="t('recommendations.moodPlaceholder')"
            :disabled="!!nextAvailableAt"
            @keydown.enter="generate"
          />
          <button class="btn-generate" :disabled="loading || !!nextAvailableAt" @click="generate">
            <span v-if="loading" class="spinner"></span>
            <span v-else>🎲 {{ t('recommendations.button') }}</span>
          </button>
        </div>

        <!-- Cache / countdown -->
        <transition name="fade">
          <div v-if="nextAvailableAt" class="cache-bar">
            <span class="cache-icon">🔒</span>
            <span>Próxima recomendação disponível em <strong>{{ countdown }}</strong></span>
          </div>
        </transition>
      </div>

      <div class="api-error" v-if="error">{{ error }}</div>

      <!-- Translating indicator -->
      <transition name="fade">
        <div v-if="translating" class="translating-bar">
          <div class="spinner-mini"></div>
          <span>Traduzindo...</span>
        </div>
      </transition>

      <!-- Movies grid -->
      <transition name="fade">
        <div v-if="movies.length" class="movies-section">
          <div class="section-title">
            <span class="gold-line"></span>
            <h2>{{ t('recommendations.title') }}</h2>
            <span class="gold-line"></span>
          </div>
          <div class="movies-grid">
            <MovieCard
              v-for="(movie, i) in movies"
              :key="movie.title"
              :movie="movie"
              :rank-class="rankClass(i)"
              :medal="rankMedal(i)"
              :label="rankLabel(i)"
              :delay="i * 0.1 + 's'"
              @click="openTrailer(movie)"
            />
          </div>
        </div>
      </transition>
    </div>

    <!-- Trailer modal -->
    <TrailerModal
      :open="trailerOpen"
      :movie="activeMovie"
      :trailer-key="trailerKey"
      :loading="trailerLoading"
      @close="closeTrailer"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import NavBar       from '@/components/NavBar.vue'
import MovieCard    from '@/components/MovieCard.vue'
import TrailerModal from '@/components/TrailerModal.vue'
import api from '@/services/api'
import { useRanks } from '@/composables/useRanks'
import { enrichMovies, fetchTrailerKey, useLocaleTranslation } from '@/composables/useMovieEnrich'

const { t, locale } = useI18n()
const auth = useAuthStore()
const { rankClass, rankMedal, rankLabel } = useRanks()

const loading        = ref(false)
const translating    = ref(false)
const error          = ref('')
const mood           = ref('')
const movies         = ref([])
const nextAvailableAt = ref(null)   // Date — quando a próxima geração é liberada
const countdown      = ref('')      // string legível "2h 30min"
let   countdownTimer = null

// Configurações do usuário para filtro e região
const userCountry   = computed(() => auth.user?.profile?.country   || 'BR')
const userPlatforms = computed(() => auth.user?.profile?.streaming_platforms || [])

const trailerOpen    = ref(false)
const trailerLoading = ref(false)
const trailerKey     = ref(null)
const activeMovie    = ref(null)

useLocaleTranslation(movies, translating)

// ── Countdown ─────────────────────────────────────────────────────────────────

function startCountdown(nextAt) {
  nextAvailableAt.value = new Date(nextAt)
  if (countdownTimer) clearInterval(countdownTimer)

  function tick() {
    const diff = nextAvailableAt.value - Date.now()
    if (diff <= 0) {
      countdown.value      = ''
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

// ── Trailer ───────────────────────────────────────────────────────────────────

async function openTrailer(movie) {
  activeMovie.value    = movie
  trailerKey.value     = null
  trailerLoading.value = true
  trailerOpen.value    = true
  document.body.style.overflow = 'hidden'
  trailerKey.value     = await fetchTrailerKey(movie.title, movie.year)
  trailerLoading.value = false
}

function closeTrailer() {
  trailerOpen.value            = false
  trailerKey.value             = null
  activeMovie.value            = null
  document.body.style.overflow = ''
}

function handleKeydown(e) {
  if (e.key === 'Escape' && trailerOpen.value) closeTrailer()
}

// ── Enrich helper ─────────────────────────────────────────────────────────────

async function enrich(rawMovies) {
  return enrichMovies(rawMovies, locale.value, {
    watchRegion:    userCountry.value,
    userPlatformIds: userPlatforms.value.length ? userPlatforms.value : null,
  })
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  window.addEventListener('keydown', handleKeydown)

  // Tenta carregar recomendação em cache das últimas 24h
  try {
    const { data } = await api.get('/recommendations/today')
    movies.value = await enrich(data.movies)
    if (data.next_available_at) startCountdown(data.next_available_at)
  } catch {} // 404 = nenhum cache, tudo certo
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
  if (countdownTimer) clearInterval(countdownTimer)
})

// ── Recommendations ───────────────────────────────────────────────────────────

async function generate() {
  loading.value = true
  error.value   = ''
  try {
    const { data } = await api.post('/recommendations', {
      mood:     mood.value || null,
      language: locale.value,
    })
    movies.value = await enrich(data.movies)
    if (data.next_available_at) startCountdown(data.next_available_at)
  } catch (e) {
    error.value = e.response?.data?.detail || t('recommendations.error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page    { min-height: 100vh; background: #08080c; font-family: 'DM Sans', sans-serif; color: #e8e0d0; }
.content { max-width: 960px; margin: 0 auto; padding: 96px 2rem 4rem; display: flex; flex-direction: column; gap: 2rem; }

.hero { padding: 1.5rem 0 0.5rem; }
h1 { font-family: 'Playfair Display', serif; font-size: 2.25rem; margin: 0 0 0.4rem; color: #e8e0d0; font-weight: 600; }
.gold { color: #d4af37; }
.hero-text p { color: #6b6050; font-size: 1rem; margin: 0; }

.prompt-card { background: #0f0f15; border: 1px solid rgba(212,175,55,0.15); border-radius: 16px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; }
.prompt-label { font-size: 0.78rem; font-weight: 500; color: #8a7a5a; letter-spacing: 0.06em; text-transform: uppercase; }
.prompt-row { display: flex; gap: 0.75rem; }
.prompt-row input { flex: 1; padding: 0.75rem 1rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; outline: none; transition: all 0.2s; }
.prompt-row input::placeholder { color: #3a3228; }
.prompt-row input:focus { border-color: rgba(212,175,55,0.35); background: rgba(212,175,55,0.03); }
.prompt-row input:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-generate { padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #d4af37, #b8860b); border: none; border-radius: 10px; color: #08080c; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; font-weight: 500; cursor: pointer; transition: all 0.2s; white-space: nowrap; display: flex; align-items: center; gap: 0.4rem; min-width: 130px; justify-content: center; }
.btn-generate:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212,175,55,0.3); }
.btn-generate:disabled { opacity: 0.4; cursor: not-allowed; }

.cache-bar { display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 1rem; background: rgba(212,175,55,0.04); border: 1px solid rgba(212,175,55,0.12); border-radius: 10px; font-size: 0.82rem; color: #6b6050; }
.cache-icon { font-size: 0.85rem; }
.cache-bar strong { color: #d4af37; }

.spinner { width: 15px; height: 15px; border: 2px solid rgba(8,8,12,0.3); border-top-color: #08080c; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.api-error { background: rgba(220,80,80,0.1); border: 1px solid rgba(220,80,80,0.3); border-radius: 10px; padding: 0.875rem 1rem; color: #e05555; font-size: 0.875rem; }

.translating-bar { display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 1rem; background: rgba(212,175,55,0.06); border: 1px solid rgba(212,175,55,0.15); border-radius: 10px; font-size: 0.82rem; color: #8a7a5a; }
.spinner-mini { width: 13px; height: 13px; border: 2px solid rgba(212,175,55,0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }

.section-title { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.section-title h2 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #d4af37; margin: 0; white-space: nowrap; font-weight: 600; }
.gold-line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent); }

.movies-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }

.fade-enter-active { transition: opacity 0.3s, transform 0.3s; }
.fade-enter-from   { opacity: 0; transform: translateY(10px); }

@media (max-width: 640px) {
  .movies-grid { grid-template-columns: 1fr; }
}
</style>