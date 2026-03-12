<template>
  <div class="page">
    <div class="bg-overlay"></div>

    <div class="card">
      <div class="card-header">
        <div class="logo">
          <img src="/logo.png" alt="CineMAGIC" class="logo-img" />
        </div>
        <h1>{{ t('login.title') }}</h1>
        <p>{{ t('login.subtitle') }}</p>
      </div>

      <form @submit.prevent="submit" class="form" novalidate>

        <div class="field" :class="{ error: touched.email && !form.email }">
          <label>{{ t('login.email') }}</label>
          <input
            v-model="form.email"
            type="email"
            :placeholder="t('login.emailPlaceholder')"
            @blur="touched.email = true"
            autocomplete="email"
          />
        </div>

        <PasswordInput
          v-model="form.password"
          :label="t('login.password')"
          :placeholder="t('login.passwordPlaceholder')"
          autocomplete="current-password"
          @blur="touched.password = true"
        />

        <router-link to="/forgot-password" class="forgot-link">
          {{ t('login.forgotPassword') }}
        </router-link>

        <div class="api-error" v-if="error">{{ error }}</div>

        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span v-else>{{ t('login.submit') }}</span>
        </button>

        <p class="register-link">
          {{ t('login.noAccount') }}
          <router-link to="/register">{{ t('login.register') }}</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import PasswordInput from '@/components/PasswordInput.vue'

const { t }  = useI18n()
const auth   = useAuthStore()
const router = useRouter()

const loading = ref(false)
const error   = ref('')
const form    = reactive({ email: '', password: '' })
const touched = reactive({ email: false, password: false })

async function submit() {
  loading.value = true
  error.value   = ''
  try {
    await auth.login(form.email, form.password)
    router.push('/recommendations')
  } catch (e) {
    error.value = e.response?.data?.detail || t('login.error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #08080c;
  padding: 2rem 1rem;
  font-family: 'DM Sans', sans-serif;
}

.bg-overlay {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(212, 175, 55, 0.04) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(180, 100, 20, 0.04) 0%, transparent 50%);
  pointer-events: none;
}

.card {
  width: 100%;
  max-width: 400px;
  background: #0f0f15;
  border: 1px solid rgba(212, 175, 55, 0.15);
  border-radius: 20px;
  padding: 2.5rem;
  position: relative;
  z-index: 1;
}

.card-header { text-align: center; margin-bottom: 2rem; }

.logo { margin-bottom: 1rem; }
.logo-img {
  width: 72px;
  height: 72px;
  object-fit: contain;
  filter: drop-shadow(0 0 12px rgba(245, 197, 24, 0.45));
}

h1 { font-family: 'Playfair Display', serif; font-size: 1.75rem; color: #d4af37; margin: 0 0 0.4rem; font-weight: 600; }
p  { color: #6b6050; font-size: 0.875rem; margin: 0; }

.form  { display: flex; flex-direction: column; gap: 1.25rem; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }

label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #8a7a5a;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
}
input::placeholder { color: #3a3228; }
input:focus { border-color: rgba(212, 175, 55, 0.4); background: rgba(212, 175, 55, 0.04); }
.field.error input { border-color: rgba(220, 80, 80, 0.4); }

.forgot-link {
  font-size: 0.82rem;
  color: #6b6050;
  text-decoration: none;
  text-align: right;
  transition: color 0.2s;
  margin-top: -0.5rem;
}
.forgot-link:hover { color: #d4af37; }

.api-error {
  background: rgba(220, 80, 80, 0.1);
  border: 1px solid rgba(220, 80, 80, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #e05555;
  font-size: 0.85rem;
}

.btn-submit {
  width: 100%;
  padding: 0.875rem;
  background: linear-gradient(135deg, #d4af37, #b8860b);
  border: none;
  border-radius: 10px;
  color: #08080c;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 0.25rem;
}
.btn-submit:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3); }
.btn-submit:disabled { opacity: 0.4; cursor: not-allowed; }

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(8,8,12,0.3);
  border-top-color: #08080c;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.register-link { text-align: center; font-size: 0.85rem; color: #5a5040; margin: 0; }
.register-link a { color: #d4af37; text-decoration: none; font-weight: 500; }
.register-link a:hover { text-decoration: underline; }
</style>