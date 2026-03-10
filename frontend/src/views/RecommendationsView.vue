<template>
  <div class="page">
    <NavBar />

    <div class="content">
      <div class="hero">
        <div class="hero-text">
          <h1>{{ t('recommendations.hello') }} <span class="gold">{{ auth.user?.name?.split(' ')[0] }}</span> 👋</h1>
          <p>{{ t('recommendations.subtitle') }}</p>
        </div>
      </div>

      <div class="prompt-card">
        <label class="prompt-label">{{ t('recommendations.label') }}</label>
        <div class="prompt-row">
          <input
            v-model="extraPrompt"
            type="text"
            :placeholder="t('recommendations.placeholder')"
            @keydown.enter="generate"
          />
          <button class="btn-generate" :disabled="loading" @click="generate">
            <span v-if="loading" class="spinner"></span>
            <span v-else>🎲 {{ t('recommendations.button') }}</span>
          </button>
        </div>
      </div>

      <div class="api-error" v-if="error">{{ error }}</div>

      <transition name="fade">
        <div v-if="movies.length" class="movies-section">
          <div class="section-title">
            <span class="gold-line"></span>
            <h2>{{ t('recommendations.title') }}</h2>
            <span class="gold-line"></span>
          </div>
          <div class="movies-grid">
            <div
              v-for="(movie, i) in movies"
              :key="movie.title"
              class="movie-card"
              :style="{ animationDelay: i * 0.08 + 's' }"
            >
              <div class="movie-poster">
                <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" loading="lazy" />
                <div v-else class="poster-placeholder"><span>🎬</span></div>
              </div>
              <div class="movie-body">
                <div class="movie-top">
                  <h3>{{ movie.title }}</h3>
                  <span class="movie-year" v-if="movie.year">{{ movie.year }}</span>
                </div>
                <span class="movie-genre">{{ movie.genre }}</span>
                <div class="ratings" v-if="movie.imdb || movie.rottenTomatoes">
                  <span class="rating imdb" v-if="movie.imdb">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg" alt="IMDb" />
                    {{ movie.imdb }}
                  </span>
                  <span class="rating rt" v-if="movie.rottenTomatoes">🍅 {{ movie.rottenTomatoes }}</span>
                </div>
                <p class="movie-desc">{{ movie.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <div v-if="history.length" class="history-section">
        <div class="section-title">
          <span class="gold-line"></span>
          <h2>{{ t('recommendations.history') }}</h2>
          <span class="gold-line"></span>
        </div>
        <div class="history-list">
          <button v-for="rec in history" :key="rec.id" class="history-item" @click="showRec(rec)">
            <div class="history-left">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
              </svg>
              <span>{{ formatDate(rec.created_at) }}</span>
            </div>
            <span class="history-badge">{{ rec.movies?.length ?? '—' }} {{ t('recommendations.movies') }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'
import api from '@/services/api'

const { t, locale } = useI18n()
const auth        = useAuthStore()
const loading     = ref(false)
const error       = ref('')
const extraPrompt = ref('')
const movies      = ref([])
const history     = ref([])

const TMDB_TOKEN   = import.meta.env.VITE_TMDB_TOKEN
const OMDB_KEY     = import.meta.env.VITE_OMDB_API_KEY
const TMDB_IMG_URL = 'https://image.tmdb.org/t/p/w342'

async function fetchPoster(title, year) {
  try {
    const { data } = await axios.get('https://api.themoviedb.org/3/search/movie', {
      headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
      params: { query: title, year: year || undefined, language: locale.value === 'pt' ? 'pt-BR' : locale.value },
    })
    const result = data.results?.[0]
    return result?.poster_path ? `${TMDB_IMG_URL}${result.poster_path}` : null
  } catch { return null }
}

async function fetchRatings(title, year) {
  try {
    const { data } = await axios.get('https://www.omdbapi.com/', {
      params: { apikey: OMDB_KEY, t: title, y: year || undefined, tomatoes: true },
    })
    if (data.Response === 'False') return {}
    const rt = data.Ratings?.find(r => r.Source === 'Rotten Tomatoes')
    return {
      imdb: data.imdbRating !== 'N/A' ? data.imdbRating : null,
      rottenTomatoes: rt?.Value || null,
    }
  } catch { return {} }
}

async function enrichMovies(list) {
  return Promise.all(
    list.map(async (movie) => {
      const [poster, ratings] = await Promise.all([
        fetchPoster(movie.title, movie.year),
        fetchRatings(movie.title, movie.year),
      ])
      return { ...movie, poster, ...ratings }
    })
  )
}

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  await loadHistory()
})

async function generate() {
  loading.value = true
  error.value   = ''
  try {
    const { data } = await api.post('/recommendations', { extra_prompt: extraPrompt.value || null })
    movies.value = await enrichMovies(data.movies)
    await loadHistory()
  } catch (e) {
    error.value = e.response?.data?.detail || t('recommendations.error')
  } finally {
    loading.value = false
  }
}

async function loadHistory() {
  try {
    const { data } = await api.get('/recommendations')
    history.value = data
  } catch {}
}

async function showRec(rec) {
  movies.value = await enrichMovies(rec.movies)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function formatDate(dt) {
  return new Date(dt).toLocaleString(
    locale.value === 'pt' ? 'pt-BR' : locale.value === 'es' ? 'es-ES' : 'en-US',
    { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }
  )
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page { min-height: 100vh; background: #08080c; font-family: 'DM Sans', sans-serif; color: #e8e0d0; }

.content {
  max-width: 960px;
  margin: 0 auto;
  padding: 96px 2rem 4rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hero { padding: 1.5rem 0 0.5rem; }

h1 { font-family: 'Playfair Display', serif; font-size: 2.25rem; margin: 0 0 0.4rem; color: #e8e0d0; font-weight: 600; }
.gold { color: #d4af37; }
.hero-text p { color: #6b6050; font-size: 1rem; margin: 0; }

.prompt-card {
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.prompt-label { font-size: 0.78rem; font-weight: 500; color: #8a7a5a; letter-spacing: 0.06em; text-transform: uppercase; }
.prompt-row { display: flex; gap: 0.75rem; }

.prompt-row input {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s;
}

.prompt-row input::placeholder { color: #3a3228; }
.prompt-row input:focus { border-color: rgba(212, 175, 55, 0.35); background: rgba(212, 175, 55, 0.03); }

.btn-generate {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  border: none;
  border-radius: 10px;
  color: #08080c;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  min-width: 130px;
  justify-content: center;
}

.btn-generate:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3); }
.btn-generate:disabled { opacity: 0.5; cursor: not-allowed; }

.spinner { width: 15px; height: 15px; border: 2px solid rgba(8,8,12,0.3); border-top-color: #08080c; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.api-error { background: rgba(220, 80, 80, 0.1); border: 1px solid rgba(220, 80, 80, 0.3); border-radius: 10px; padding: 0.875rem 1rem; color: #e05555; font-size: 0.875rem; }

.section-title { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem; }
.section-title h2 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #d4af37; margin: 0; white-space: nowrap; font-weight: 600; }
.gold-line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent); }

.movies-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1.25rem; }

.movie-card {
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.1);
  border-radius: 14px;
  overflow: hidden;
  transition: all 0.25s;
  animation: slideUp 0.4s ease both;
  display: flex;
  flex-direction: column;
}

.movie-card:hover { border-color: rgba(212, 175, 55, 0.3); transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.5); }

@keyframes slideUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }

.movie-poster { width: 100%; aspect-ratio: 2/3; overflow: hidden; background: #1a1a22; }
.movie-poster img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.4s ease; }
.movie-card:hover .movie-poster img { transform: scale(1.04); }
.poster-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 3rem; background: linear-gradient(135deg, #1a1a22, #0f0f15); }

.movie-body { padding: 0.875rem; display: flex; flex-direction: column; gap: 0.4rem; flex: 1; }
.movie-top { display: flex; align-items: baseline; gap: 0.4rem; flex-wrap: wrap; }
.movie-top h3 { font-family: 'Playfair Display', serif; font-size: 0.95rem; color: #e8e0d0; margin: 0; font-weight: 600; line-height: 1.3; }
.movie-year { font-size: 0.75rem; color: #6b6050; white-space: nowrap; }
.movie-genre { display: inline-block; font-size: 0.7rem; color: #d4af37; background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 50px; padding: 0.18rem 0.55rem; width: fit-content; }

.ratings { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.1rem; }
.rating { display: flex; align-items: center; gap: 0.3rem; font-size: 0.75rem; font-weight: 500; padding: 0.2rem 0.5rem; border-radius: 6px; }
.rating.imdb { background: rgba(245, 197, 24, 0.1); border: 1px solid rgba(245, 197, 24, 0.2); color: #f5c518; }
.rating.imdb img { height: 12px; width: auto; }
.rating.rt { background: rgba(250, 80, 80, 0.08); border: 1px solid rgba(250, 80, 80, 0.2); color: #fa7070; }

.movie-desc { font-size: 0.8rem; color: #6b6050; line-height: 1.5; margin: 0; }

.history-list { display: flex; flex-direction: column; gap: 0.5rem; }

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1.25rem;
  background: #0f0f15;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'DM Sans', sans-serif;
  width: 100%;
  text-align: left;
}

.history-item:hover { border-color: rgba(212, 175, 55, 0.2); background: rgba(212, 175, 55, 0.04); }
.history-left { display: flex; align-items: center; gap: 0.6rem; font-size: 0.85rem; color: #6b6050; }
.history-badge { font-size: 0.78rem; color: #d4af37; background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 50px; padding: 0.2rem 0.65rem; }

.fade-enter-active { transition: opacity 0.3s, transform 0.3s; }
.fade-enter-from { opacity: 0; transform: translateY(10px); }
</style>