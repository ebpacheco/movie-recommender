<template>
  <div class="page">
    <div class="bg-overlay"></div>

    <div class="card">
      <div class="card-header">
        <div class="logo">
          <img src="/logo.png" alt="CineMAGIC" class="logo-img" />
        </div>
        <h1>{{ t('register.title') }}</h1>
        <p>{{ t('register.subtitle') }}</p>
      </div>

      <form @submit.prevent="handleRegister" class="form" novalidate>

        <!-- Nome -->
        <div class="field" :class="{ error: errors.name, success: touched.name && !errors.name }">
          <label>{{ t('register.name') }}</label>
          <input v-model="form.name" type="text" :placeholder="t('register.namePlaceholder')"
            @blur="touch('name'); validateName()"
            @input="touched.name && validateName()" />
          <span class="field-msg" v-if="errors.name">{{ errors.name }}</span>
        </div>

        <!-- Email -->
        <div class="field" :class="{ error: errors.email, success: touched.email && !errors.email }">
          <label>{{ t('register.email') }}</label>
          <input v-model="form.email" type="email" :placeholder="t('register.emailPlaceholder')"
            @blur="touch('email'); validateEmail()"
            @input="touched.email && validateEmail()" />
          <span class="field-msg" v-if="errors.email">{{ errors.email }}</span>
        </div>

        <!-- CPF -->
        <div class="field" :class="{ error: errors.cpf, success: touched.cpf && !errors.cpf }">
          <label>{{ t('register.cpf') }}</label>
          <input v-model="form.cpf" type="text" :placeholder="t('register.cpfPlaceholder')"
            maxlength="14"
            @blur="touch('cpf'); validateCpf()"
            @input="formatCpf" />
          <span class="field-msg" v-if="errors.cpf">{{ errors.cpf }}</span>
        </div>

        <!-- Senha -->
        <PasswordInput
          v-model="form.password"
          :label="t('register.password')"
          :placeholder="t('register.passwordPlaceholder')"
          autocomplete="new-password"
          :has-error="!!errors.password"
          :has-success="touched.password && !errors.password"
          @blur="touch('password'); validatePassword()"
        >
          <div class="password-rules" v-if="touched.password || form.password">
            <div class="rule" :class="{ ok: rules.length }">
              <span class="rule-dot"></span>{{ t('register.rules.length') }}
            </div>
            <div class="rule" :class="{ ok: rules.upper }">
              <span class="rule-dot"></span>{{ t('register.rules.upper') }}
            </div>
            <div class="rule" :class="{ ok: rules.number }">
              <span class="rule-dot"></span>{{ t('register.rules.number') }}
            </div>
            <div class="rule" :class="{ ok: rules.special }">
              <span class="rule-dot"></span>{{ t('register.rules.special') }}
            </div>
          </div>
        </PasswordInput>

        <!-- Confirmar senha -->
        <PasswordInput
          v-model="form.confirmPassword"
          :label="t('register.confirmPassword')"
          :placeholder="t('register.confirmPlaceholder')"
          autocomplete="new-password"
          :has-error="!!errors.confirmPassword"
          :has-success="touched.confirmPassword && !errors.confirmPassword"
          @blur="touch('confirmPassword'); validateConfirm()"
        >
          <span class="field-msg" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
        </PasswordInput>

        <div class="api-error" v-if="apiError">{{ apiError }}</div>

        <button type="submit" class="btn-submit" :disabled="loading || !isFormValid">
          <span v-if="loading" class="spinner"></span>
          <span v-else>{{ t('register.submit') }}</span>
        </button>

        <p class="login-link">
          {{ t('register.hasAccount') }}
          <router-link to="/login">{{ t('register.login') }}</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import PasswordInput from '@/components/PasswordInput.vue'

const { t }  = useI18n()
const router = useRouter()
const auth   = useAuthStore()

const form    = reactive({ name: '', email: '', cpf: '', password: '', confirmPassword: '' })
const errors  = reactive({ name: '', email: '', cpf: '', password: '', confirmPassword: '' })
const touched = reactive({ name: false, email: false, cpf: false, password: false, confirmPassword: false })
const loading  = ref(false)
const apiError = ref('')

const rules = computed(() => ({
  length:  form.password.length >= 8,
  upper:   /[A-Z]/.test(form.password),
  number:  /[0-9]/.test(form.password),
  special: /[!@#$%^&*(),.?":{}|<>]/.test(form.password),
}))

const isPasswordValid = computed(() => Object.values(rules.value).every(Boolean))

const isFormValid = computed(() =>
  form.name && form.email && form.cpf && isPasswordValid.value &&
  form.password === form.confirmPassword &&
  !Object.values(errors).some(Boolean)
)

function touch(field) { touched[field] = true }

function validateName()     { errors.name    = form.name.trim().length < 2 ? t('register.errors.name') : '' }
function validateEmail()    { errors.email   = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) ? '' : t('register.errors.email') }
function validateCpf()      { errors.cpf     = form.cpf.replace(/\D/g, '').length !== 11 ? t('register.errors.cpf') : '' }
function validatePassword() { errors.password = isPasswordValid.value ? '' : t('register.errors.password') }
function validateConfirm()  { errors.confirmPassword = form.password !== form.confirmPassword ? t('register.errors.confirmPassword') : '' }

function formatCpf() {
  let v = form.cpf.replace(/\D/g, '')
  if      (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{0,2})/, '$1.$2.$3-$4')
  else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{0,3})/, '$1.$2.$3')
  else if (v.length > 3) v = v.replace(/(\d{3})(\d{0,3})/, '$1.$2')
  form.cpf = v
  touched.cpf && validateCpf()
}

async function handleRegister() {
  touch('name'); touch('email'); touch('cpf'); touch('password'); touch('confirmPassword')
  validateName(); validateEmail(); validateCpf(); validatePassword(); validateConfirm()
  if (!isFormValid.value) return

  loading.value  = true
  apiError.value = ''
  try {
    await auth.register({
      name:     form.name,
      email:    form.email,
      cpf:      form.cpf.replace(/\D/g, ''),
      password: form.password,
    })
    router.push('/recommendations')
  } catch (e) {
    apiError.value = e.response?.data?.detail || 'Erro ao criar conta. Tente novamente.'
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
  max-width: 440px;
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

h1 { font-family: 'Playfair Display', serif; font-size: 1.75rem; color: #e8e0d0; margin: 0 0 0.5rem; font-weight: 600; }
p  { color: #6b6050; font-size: 0.875rem; line-height: 1.5; margin: 0; }

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
input:focus   { border-color: rgba(212, 175, 55, 0.4); background: rgba(212, 175, 55, 0.04); }
.field.error   input { border-color: rgba(220, 80, 80, 0.5); }
.field.success input { border-color: rgba(80, 200, 120, 0.3); }

.field-msg { font-size: 0.78rem; color: #e05555; }

.password-rules { display: flex; flex-direction: column; gap: 0.3rem; margin-top: 0.35rem; }

.rule {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: #5a5040;
  transition: color 0.2s;
}
.rule.ok { color: #50c878; }
.rule-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; flex-shrink: 0; }

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
  gap: 0.5rem;
  margin-top: 0.5rem;
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

.login-link { text-align: center; font-size: 0.85rem; color: #5a5040; margin: 0; }
.login-link a { color: #d4af37; text-decoration: none; font-weight: 500; }
.login-link a:hover { text-decoration: underline; }
</style>