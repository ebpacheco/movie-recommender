<template>
  <div class="page">
    <div class="content">
      <div class="card">
        <!-- Logo -->
        <div class="logo">
          <span class="logo-icon">🎬</span>
          <span class="logo-text">Cine<span class="gold">MAGIC</span></span>
        </div>

        <!-- Token inválido / sem token -->
        <template v-if="!token">
          <div class="error-box">
            <div class="error-icon">⚠️</div>
            <h2>{{ t('resetPassword.invalidTitle') }}</h2>
            <p>{{ t('resetPassword.invalidMessage') }}</p>
          </div>
          <router-link to="/forgot-password" class="btn-submit" style="text-decoration:none;text-align:center;">
            {{ t('resetPassword.requestNew') }}
          </router-link>
        </template>

        <!-- Formulário -->
        <template v-else-if="!success">
          <h1>{{ t('resetPassword.title') }}</h1>
          <p class="subtitle">{{ t('resetPassword.subtitle') }}</p>

          <form @submit.prevent="handleSubmit">
            <!-- Nova senha -->
            <div class="field" :class="{ error: errors.password }">
              <label>{{ t('resetPassword.passwordLabel') }}</label>
              <div class="input-wrap">
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  :placeholder="t('resetPassword.passwordPlaceholder')"
                  autocomplete="new-password"
                  @input="validatePassword"
                />
                <button type="button" class="toggle-eye" @click="showPassword = !showPassword">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
              <span class="field-msg" v-if="errors.password">{{ errors.password }}</span>

              <!-- Regras de senha -->
              <div class="rules">
                <div class="rule" :class="{ ok: rules.length }"><span class="dot"></span>{{ t('register.rules.length') }}</div>
                <div class="rule" :class="{ ok: rules.upper }"><span class="dot"></span>{{ t('register.rules.upper') }}</div>
                <div class="rule" :class="{ ok: rules.number }"><span class="dot"></span>{{ t('register.rules.number') }}</div>
                <div class="rule" :class="{ ok: rules.special }"><span class="dot"></span>{{ t('register.rules.special') }}</div>
              </div>
            </div>

            <!-- Confirmar senha -->
            <div class="field" :class="{ error: errors.confirm }">
              <label>{{ t('resetPassword.confirmLabel') }}</label>
              <div class="input-wrap">
                <input
                  v-model="confirm"
                  :type="showConfirm ? 'text' : 'password'"
                  :placeholder="t('resetPassword.confirmPlaceholder')"
                  autocomplete="new-password"
                  @input="validateConfirm"
                />
                <button type="button" class="toggle-eye" @click="showConfirm = !showConfirm">
                  {{ showConfirm ? '🙈' : '👁️' }}
                </button>
              </div>
              <span class="field-msg" v-if="errors.confirm">{{ errors.confirm }}</span>
            </div>

            <div class="api-error" v-if="apiError">{{ apiError }}</div>

            <button type="submit" class="btn-submit" :disabled="loading || !isValid">
              <span v-if="loading" class="spinner"></span>
              <span v-else>{{ t('resetPassword.submit') }}</span>
            </button>
          </form>
        </template>

        <!-- Sucesso -->
        <template v-else>
          <div class="success-box">
            <div class="success-icon">✅</div>
            <h2>{{ t('resetPassword.successTitle') }}</h2>
            <p>{{ t('resetPassword.successMessage') }}</p>
          </div>
          <router-link to="/login" class="btn-submit" style="text-decoration:none;text-align:center;">
            {{ t('resetPassword.goToLogin') }}
          </router-link>
        </template>

        <router-link v-if="!success" to="/login" class="back-link">
          ← {{ t('forgotPassword.backToLogin') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'

const { t }   = useI18n()
const route   = useRoute()
const token   = route.query.token || ''

const password     = ref('')
const confirm      = ref('')
const showPassword = ref(false)
const showConfirm  = ref(false)
const loading      = ref(false)
const success      = ref(false)
const apiError     = ref('')
const errors       = ref({ password: '', confirm: '' })

const rules = computed(() => ({
  length:  password.value.length >= 8,
  upper:   /[A-Z]/.test(password.value),
  number:  /[0-9]/.test(password.value),
  special: /[^A-Za-z0-9]/.test(password.value),
}))

const isPasswordValid = computed(() => Object.values(rules.value).every(Boolean))

const isValid = computed(() =>
  isPasswordValid.value && password.value === confirm.value
)

function validatePassword() {
  errors.value.password = isPasswordValid.value ? '' : t('register.errors.password')
}

function validateConfirm() {
  errors.value.confirm = password.value !== confirm.value
    ? t('register.errors.confirmPassword') : ''
}

async function handleSubmit() {
  validatePassword()
  validateConfirm()
  if (!isValid.value) return

  loading.value  = true
  apiError.value = ''
  try {
    await api.post('/auth/reset-password', { token, password: password.value })
    success.value = true
  } catch (e) {
    apiError.value = e.response?.data?.detail || t('resetPassword.errorGeneric')
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

.input-wrap { position: relative; }
.input-wrap input { width: 100%; padding: 0.75rem 2.75rem 0.75rem 1rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; color: #e8e0d0; font-family: 'DM Sans', sans-serif; font-size: 0.95rem; outline: none; transition: all 0.2s; }
.input-wrap input::placeholder { color: #3a3228; }
.input-wrap input:focus { border-color: rgba(212,175,55,0.35); background: rgba(212,175,55,0.03); }
.toggle-eye { position: absolute; right: 0.75rem; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0; line-height: 1; }

.field.error .input-wrap input { border-color: rgba(220,80,80,0.5); }
.field-msg { font-size: 0.78rem; color: #e05555; }

.rules { display: grid; grid-template-columns: 1fr 1fr; gap: 0.3rem 1rem; margin-top: 0.25rem; }
.rule { display: flex; align-items: center; gap: 0.4rem; font-size: 0.75rem; color: #4a4038; transition: color 0.2s; }
.rule.ok { color: #5a9a6a; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; flex-shrink: 0; }

.btn-submit { padding: 0.875rem; background: linear-gradient(135deg, #d4af37, #b8860b); border: none; border-radius: 10px; color: #08080c; font-family: 'DM Sans', sans-serif; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.btn-submit:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212,175,55,0.3); }
.btn-submit:disabled { opacity: 0.4; cursor: not-allowed; }

.api-error { background: rgba(220,80,80,0.1); border: 1px solid rgba(220,80,80,0.3); border-radius: 10px; padding: 0.875rem 1rem; color: #e05555; font-size: 0.875rem; }

.success-box, .error-box { text-align: center; display: flex; flex-direction: column; align-items: center; gap: 0.75rem; padding: 1rem 0; }
.success-icon, .error-icon { font-size: 3rem; }
.success-box h2 { font-family: 'Playfair Display', serif; color: #d4af37; font-size: 1.2rem; margin: 0; }
.error-box h2 { font-family: 'Playfair Display', serif; color: #e05555; font-size: 1.2rem; margin: 0; }
.success-box p, .error-box p { color: #8a7a5a; font-size: 0.9rem; margin: 0; line-height: 1.6; }

.back-link { color: #6b6050; font-size: 0.85rem; text-decoration: none; text-align: center; transition: color 0.2s; }
.back-link:hover { color: #d4af37; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(8,8,12,0.3); border-top-color: #08080c; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>