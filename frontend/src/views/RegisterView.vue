<template>
  <div class="container">
    <h1>🎬 Movie Recommender</h1>
    <h2>Criar conta</h2>

    <div v-if="error" class="error">{{ error }}</div>

    <div class="form">
      <input v-model="form.name"     type="text"     placeholder="Nome completo" />
      <input v-model="form.email"    type="email"    placeholder="E-mail" />
      <input v-model="form.cpf"      type="text"     placeholder="CPF (somente números)" maxlength="11" />
      <input v-model="form.password" type="password" placeholder="Senha" />

      <hr />
      <p><strong>Suas preferências de cinema</strong></p>

      <input v-model="genresInput"    type="text" placeholder="Gêneros favoritos (ex: Ação, Drama)" />
      <input v-model="moviesInput"    type="text" placeholder="Filmes favoritos (ex: Matrix, Interstellar)" />
      <input v-model="actorsInput"    type="text" placeholder="Atores favoritos (ex: Tom Hanks, Meryl Streep)" />
      <input v-model="directorsInput" type="text" placeholder="Diretores favoritos (ex: Nolan, Spielberg)" />

      <small>Separe os itens por vírgula</small>

      <button :disabled="loading" @click="submit">
        {{ loading ? 'Cadastrando...' : 'Criar conta' }}
      </button>
    </div>

    <p>Já tem conta? <router-link to="/login">Entrar</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth    = useAuthStore()
const router  = useRouter()
const loading = ref(false)
const error   = ref('')

const form           = ref({ name: '', email: '', cpf: '', password: '' })
const genresInput    = ref('')
const moviesInput    = ref('')
const actorsInput    = ref('')
const directorsInput = ref('')

const split = (str) => str.split(',').map(s => s.trim()).filter(Boolean)

async function submit() {
  loading.value = true
  error.value   = ''
  try {
    await auth.register({
      ...form.value,
      profile: {
        favorite_genres:    split(genresInput.value),
        favorite_movies:    split(moviesInput.value),
        favorite_actors:    split(actorsInput.value),
        favorite_directors: split(directorsInput.value),
      },
    })
    router.push('/recommendations')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao cadastrar'
  } finally {
    loading.value = false
  }
}
</script>
