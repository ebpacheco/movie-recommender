<template>
  <div class="page">
    <div class="content">
      <div class="card">
        <div class="logo">
          <span class="logo-icon">🎬</span>
          <span class="logo-text">Cine<span class="gold">MAGIC</span></span>
        </div>

        <!-- Processando -->
        <template v-if="status === 'loading'">
          <div class="spinner-wrap">
            <div class="spinner-gold"></div>
          </div>
          <p class="subtitle">{{ t('verifyEmail.verifying') }}</p>
        </template>

        <!-- Sucesso -->
        <template v-else-if="status === 'success'">
          <div class="result-box">
            <div class="result-icon">✅</div>
            <h2>{{ t('verifyEmail.successTitle') }}</h2>
            <p>{{ t('verifyEmail.successMessage') }}</p>
          </div>
          <router-link to="/login" class="btn-submit" style="text-decoration:none;text-align:center;">
            {{ t('verifyEmail.goToLogin') }}
          </router-link>
        </template>

        <!-- Erro -->
        <template v-else>
          <div class="result-box">
            <div class="result-icon">⚠️</div>
            <h2 class="error">{{ t('verifyEmail.errorTitle') }}</h2>
            <p>{{ t('verifyEmail.errorMessage') }}</p>
          </div>
          <button class="btn-submit" :disabled="resending" @click="resendVerification">
            <span v-if="resending" class="spinner-sm"></span>
            <span v-else>{{ t('verifyEmail.resend') }}</span>
          </button>
          <router-link to="/login" class="back-link">
            ← {{ t('forgotPassword.backToLogin') }}
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute }       from 'vue-router'
import { useI18n }        from 'vue-i18n'
import api                from '@/services/api'

const { t }  = useI18n()
const route  = useRoute()
const token  = route.query.token || ''
const email  = route.query.email || ''

const status   = ref('loading')
const resending = ref(false)

onMounted(async () => {
  if (!token) { status.value = 'error'; return }
  try {
    await api.post(`/auth/verify-email?token=${token}`)
    status.value = 'success'
  } catch {
    status.value = 'error'
  }
})

async function resendVerification() {
  if (!email) return
  resending.value = true
  try {
    await api.post('/auth/resend-verification', { email })
  } catch {}
  finally { resending.value = false }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page    { min-height: 100vh; background: #08080c; display: flex; align-items: center; justify-content: center; font-family: 'DM Sans', sans-serif; padding: 2rem 1rem; }
.content { width: 100%; max-width: 420px; }

.card { background: #0f0f15; border: 1px solid rgba(212,175,55,0.15); border-radius: 20px; padding: 2.5rem 2rem; display: flex; flex-direction: column; gap: 1.25rem; align-items: center; text-align: center; }

.logo { display: flex; align-items: center; gap: 0.5rem; }
.logo-icon { font-size: 1.5rem; }
.logo-text { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #e8e0d0; font-weight: 600; }
.gold { color: #d4af37; }

.spinner-wrap  { padding: 1rem 0; }
.spinner-gold  { width: 40px; height: 40px; border: 3px solid rgba(212,175,55,0.15); border-top-color: #d4af37; border-radius: 50%; animation: spin 0.8s linear infinite; }

.subtitle { color: #6b6050; font-size: 0.9rem; margin: 0; }

.result-box    { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; padding: 0.5rem 0; }
.result-icon   { font-size: 3rem; }
.result-box h2 { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #d4af37; margin: 0; }
.result-box h2.error { color: #e05555; }
.result-box p  { color: #8a7a5a; font-size: 0.9rem; margin: 0; line-height: 1.6; }

.btn-submit { width: 100%; padding: 0.875rem; background: linear-gradient(135deg, #d4af37, #b8860b); border: none; border-radius: 10px; color: #08080c; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.btn-submit:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212,175,55,0.3); }
.btn-submit:disabled { opacity: 0.4; cursor: not-allowed; }

.spinner-sm { width: 16px; height: 16px; border: 2px solid rgba(8,8,12,0.3); border-top-color: #08080c; border-radius: 50%; animation: spin 0.6s linear infinite; }

.back-link { color: #6b6050; font-size: 0.85rem; text-decoration: none; transition: color 0.2s; }
.back-link:hover { color: #d4af37; }

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 480px) {
  .card { padding: 1.75rem 1.25rem; }
}
</style>
