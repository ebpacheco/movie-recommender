<template>
  <div class="page">
    <div class="bg-overlay"></div>

    <div class="card">
      <div class="card-header">
        <img src="/logo.svg" alt="CineMAGIC" class="logo-img" />
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

        <!-- Data de nascimento -->
        <div class="field" :class="{ error: errors.birthDate, success: touched.birthDate && !errors.birthDate }">
          <label>{{ t('register.birthDate') }}</label>
          <input v-model="form.birthDate" type="date"
            :max="maxBirthDate"
            @blur="touch('birthDate'); validateBirthDate()"
            @input="touched.birthDate && validateBirthDate()" />
          <span class="field-msg" v-if="errors.birthDate">{{ errors.birthDate }}</span>
        </div>

        <!-- País -->
        <div class="field">
          <label>{{ t('register.country') }}</label>
          <div class="select-wrapper">
            <select v-model="form.country" class="country-select">
              <option v-for="c in COUNTRIES" :key="c.code" :value="c.code">
                {{ c.flag }} {{ c.name }}
              </option>
            </select>
            <span class="select-arrow">▾</span>
          </div>
          <span class="field-hint">{{ t('register.countryHint') }}</span>
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
import { useI18n } from 'vue-i18n'
import PasswordInput      from '@/components/PasswordInput.vue'
import { useRegisterForm } from '@/composables/useRegisterForm'

const { t } = useI18n()

const {
  form, errors, touched, loading, apiError,
  rules, isFormValid,
  touch, validateName, validateEmail, validateBirthDate, validatePassword, validateConfirm,
  handleRegister,
} = useRegisterForm()

// Data máxima = hoje (não permite data futura)
const maxBirthDate = new Date().toISOString().split('T')[0]

const COUNTRIES = [
  { code: 'BR', name: 'Brasil',          flag: '🇧🇷' },
  { code: 'US', name: 'United States',   flag: '🇺🇸' },
  { code: 'GB', name: 'United Kingdom',  flag: '🇬🇧' },
  { code: 'PT', name: 'Portugal',        flag: '🇵🇹' },
  { code: 'AR', name: 'Argentina',       flag: '🇦🇷' },
  { code: 'MX', name: 'México',          flag: '🇲🇽' },
  { code: 'CO', name: 'Colômbia',        flag: '🇨🇴' },
  { code: 'CL', name: 'Chile',           flag: '🇨🇱' },
  { code: 'PE', name: 'Peru',            flag: '🇵🇪' },
  { code: 'CA', name: 'Canadá',          flag: '🇨🇦' },
  { code: 'AU', name: 'Austrália',       flag: '🇦🇺' },
  { code: 'FR', name: 'França',          flag: '🇫🇷' },
  { code: 'DE', name: 'Alemanha',        flag: '🇩🇪' },
  { code: 'ES', name: 'Espanha',         flag: '🇪🇸' },
  { code: 'IT', name: 'Itália',          flag: '🇮🇹' },
  { code: 'JP', name: 'Japão',           flag: '🇯🇵' },
  { code: 'KR', name: 'Coreia do Sul',   flag: '🇰🇷' },
  { code: 'IN', name: 'Índia',           flag: '🇮🇳' },
]
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

.logo-img {
  width: 72px;
  height: 72px;
  object-fit: contain;
  filter: drop-shadow(0 0 12px rgba(245, 197, 24, 0.45));
  margin-bottom: 1rem;
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
input:focus    { border-color: rgba(212, 175, 55, 0.4); background: rgba(212, 175, 55, 0.04); }
.field.error   input { border-color: rgba(220, 80, 80, 0.5); }
.field.success input { border-color: rgba(80, 200, 120, 0.3); }

/* Country select */
.select-wrapper { position: relative; }
.country-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #e8e0d0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  outline: none;
  appearance: none;
  cursor: pointer;
  transition: all 0.2s;
}
.country-select:focus { border-color: rgba(212, 175, 55, 0.4); background: rgba(212, 175, 55, 0.04); }
.country-select option { background: #0f0f15; color: #e8e0d0; }
.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #5a5040;
  pointer-events: none;
  font-size: 0.75rem;
}
.field-hint { font-size: 0.75rem; color: #3a3228; }

.field-msg { font-size: 0.78rem; color: #e05555; }

.password-rules { display: flex; flex-direction: column; gap: 0.3rem; margin-top: 0.35rem; }
.rule { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; color: #5a5040; transition: color 0.2s; }
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