<template>
  <div class="container">
    <header>
      <h1>🎬 Movie Recommender</h1>
      <button class="logout" @click="logout">Sair</button>
    </header>

    <p v-if="auth.user">Olá, <strong>{{ auth.user.name }}</strong>!</p>

    <div class="prompt-box">
      <input
        v-model="extraPrompt"
        type="text"
        placeholder="Contexto extra (ex: quero algo leve pra hoje à noite...)"
      />
      <button :disabled="loading" @click="generate">
        {{ loading ? 'Gerando...' : '🎲 Recomendar filmes' }}
      </button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="movies.length" class="movies">
      <div v-for="movie in movies" :key="movie.title" class="movie-card">
        <h3>{{ movie.title }} <span v-if="movie.year">({{ movie.year }})</span></h3>
        <p class="genre">🎭 {{ movie.genre }}</p>
        <p>{{ movie.description }}</p>
      </div>
    </div>

    <hr v-if="history.length" />

    <div v-if="history.length">
      <h2>Histórico</h2>
      <div v-for="rec in history" :key="rec.id" class="history-item" @click="showRec(rec)">
        <span>{{ formatDate(rec.created_at) }}</span>
        <span>{{ rec.movies.length }} filmes</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const auth        = useAuthStore()
const router      = useRouter()
const loading     = ref(false)
const error       = ref('')
const extraPrompt = ref('')
const movies      = ref([])
const history     = ref([])

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  await loadHistory()
})

async function generate() {
  loading.value = true
  error.value   = ''
  try {
    const { data } = await api.post('/recommendations', { extra_prompt: extraPrompt.value || null })
    movies.value = data.movies
    await loadHistory()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao gerar recomendações'
  } finally {
    loading.value = false
  }
}

async function loadHistory() {
  const { data } = await api.get('/recommendations')
  history.value  = data
}

function showRec(rec) {
  movies.value = rec.movies
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function formatDate(dt) {
  return new Date(dt).toLocaleString('pt-BR')
}

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
