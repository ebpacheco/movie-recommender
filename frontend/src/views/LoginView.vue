<template>
  <div class="container">
    <h1>🎬 Movie Recommender</h1>
    <h2>Entrar</h2>

    <div v-if="error" class="error">{{ error }}</div>

    <div class="form">
      <input v-model="form.email"    type="email"    placeholder="E-mail" />
      <input v-model="form.password" type="password" placeholder="Senha"  />
      <button :disabled="loading" @click="submit">
        {{ loading ? 'Entrando...' : 'Entrar' }}
      </button>
    </div>

    <p>Não tem conta? <router-link to="/register">Cadastre-se</router-link></p>
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
const form    = ref({ email: '', password: '' })

async function submit() {
  loading.value = true
  error.value   = ''
  try {
    await auth.login(form.value.email, form.value.password)
    router.push('/recommendations')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao entrar'
  } finally {
    loading.value = false
  }
}
</script>
