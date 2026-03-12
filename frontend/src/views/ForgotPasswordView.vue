<template>
  <div class="page">
    <div class="content">
      <div class="card">
        <!-- Logo -->
        <div class="logo">
          <span class="logo-icon">🎬</span>
          <span class="logo-text">Cine<span class="gold">MAGIC</span></span>
        </div>

        <template v-if="!sent">
          <h1>{{ t('forgotPassword.title') }}</h1>
          <p class="subtitle">{{ t('forgotPassword.subtitle') }}</p>

          <form @submit.prevent="handleSubmit">
            <div class="field" :class="{ error: error }">
              <label>{{ t('forgotPassword.emailLabel') }}</label>
              <input
                v-model="email"
                type="email"
                :placeholder="t('forgotPassword.emailPlaceholder')"
                autocomplete="email"
                autofocus
              />
              <span class="field-msg" v-if="error">{{ error }}</span>
            </div>

            <button type="submit" class="btn-submit" :disabled="loading || !email">
              <span v-if="loading" class="spinner"></span>
              <span v-else>{{ t('forgotPassword.submit') }}</span>
            </button>
          </form>
        </template>

        <!-- Sucesso -->
        <template v-else>
          <div class="success-box">
            <div class="success-icon">✉️</div>
            <h2>{{ t('forgotPassword.sentTitle') }}</h2>
            <p>{{ t('forgotPassword.sentMessage') }}</p>
            <p class="hint">{{ t('forgotPassword.sentHint') }}</p>
          </div>
        </template>

        <router-link to="/login" class="back-link">
          ← {{ t('forgotPassword.backToLogin') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'

const { t } = useI18n()

const email   = ref('')
const loading = ref(false)
const error   = ref('')
const sent    = ref(false)

async function handleSubmit() {
  if (!email.value) return
  loading.value = true
  error.value   = ''
  try {
    await api.post('/auth/forgot-password', { email: email.value })
    sent.value = true
  } catch {
    // Mesmo em erro, mostramos sucesso para não revelar se o e-mail existe
    sent.value = true
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page    { min-height: 100vh; background: #08080c; display: flex; align-items: center; justify-content: center; font-family: 'DM Sans', sans-serif; padding: 2rem; }
.content { width: 100%; max-width: 420px; }

.card { background: #0f0f15; border: 1px solid rgba(212,175,55,0.15); border-radius: 20px; padding: 2.5rem 2rem; display: flex; flex-direction: column; gap: 1.25rem; }

.logo { display: flex; align-items: center; gap: 0.5rem; justify-content: center; margin-bottom: 0.5rem; }
.logo-icon { font-size: 1.5rem; }
.logo-text { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #e8e0d0; font-weight: 600; letter-spacing: 0.04em; }
.gold { color: #d4af37; }

h1 { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #e8e0d0; margin: 0; text-align: center; }
.subtitle { color: #6b6050; font-size: 0.9rem; text-align: center; margin: 0; line-height: 1.5; }

form { display: flex; flex-direction: column; gap: 1rem; }

.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field label { font-size: 0.78rem; font-weight: 500; color: #8a7a5a; letter-spacing: 0.06em; text-transform: uppercase; }
.field input { padding: 0.75rem 1rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.95rem; outline: none; transition: all 0.2s; }
.field input::placeholder { color: #3a3228; }
.field input:focus { border-color: rgba(212,175,55,0.35); background: rgba(212,175,55,0.03); }
.field.error input { border-color: rgba(220,80,80,0.5); }
.field-msg { font-size: 0.78rem; color: #e05555; }

.btn-submit { padding: 0.875rem; background: linear-gradient(135deg, #d4af37, #b8860b); border: none; border-radius: 10px; color: #08080c; font-family: 'DM Sans', sans-serif; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.btn-submit:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212,175,55,0.3); }
.btn-submit:disabled { opacity: 0.4; cursor: not-allowed; }

.success-box { text-align: center; display: flex; flex-direction: column; align-items: center; gap: 0.75rem; padding: 1rem 0; }
.success-icon { font-size: 3rem; }
.success-box h2 { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #d4af37; margin: 0; }
.success-box p { color: #8a7a5a; font-size: 0.9rem; margin: 0; line-height: 1.6; }
.success-box .hint { color: #4a4038; font-size: 0.8rem; }

.back-link { color: #6b6050; font-size: 0.85rem; text-decoration: none; text-align: center; transition: color 0.2s; }
.back-link:hover { color: #d4af37; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(8,8,12,0.3); border-top-color: #08080c; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>