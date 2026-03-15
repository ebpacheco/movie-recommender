// src/composables/useRegisterForm.js
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { detectCountry } from '@/composables/useCountryDetect'

export function useRegisterForm() {
  const { t }  = useI18n()
  const router = useRouter()
  const auth   = useAuthStore()

  const form = reactive({
    name:            '',
    email:           '',
    password:        '',
    confirmPassword: '',
    country:         'BR',
    birthDate:       '',
    termsAccepted:   false,
    privacyAccepted: false,
  })

  const errors = reactive({
    name:            '',
    email:           '',
    password:        '',
    confirmPassword: '',
    birthDate:       '',
    terms:           '',
    privacy:         '',
  })

  const touched = reactive({
    name:            false,
    email:           false,
    password:        false,
    confirmPassword: false,
    birthDate:       false,
    terms:           false,
    privacy:         false,
  })

  const loading    = ref(false)
  const apiError   = ref('')
  const registered = ref(false)

  // País fixo BR como padrão

  // ── Regras de senha ──────────────────────────────────────────────────────────

  const rules = computed(() => ({
    length:  form.password.length >= 8,
    upper:   /[A-Z]/.test(form.password),
    number:  /[0-9]/.test(form.password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(form.password),
  }))

  const isPasswordValid = computed(() => Object.values(rules.value).every(Boolean))

  const isFormValid = computed(() =>
    form.name.trim().length >= 2 &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) &&
    form.birthDate &&
    form.termsAccepted &&
    form.privacyAccepted &&
    isPasswordValid.value &&
    form.password === form.confirmPassword
  )

  // ── Validações ───────────────────────────────────────────────────────────────

  function touch(field) { touched[field] = true }

  function validateName() {
    errors.name = form.name.trim().length < 2 ? t('register.errors.name') : ''
  }

  function validateEmail() {
    errors.email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)
      ? '' : t('register.errors.email')
  }

  function validateBirthDate() {
    if (!form.birthDate) {
      errors.birthDate = t('register.errors.birthDate')
      return
    }
    const birth = new Date(form.birthDate)
    const today = new Date()
    const age   = today.getFullYear() - birth.getFullYear()
    const hasBirthdayPassed =
      today.getMonth() > birth.getMonth() ||
      (today.getMonth() === birth.getMonth() && today.getDate() >= birth.getDate())
    const realAge = hasBirthdayPassed ? age : age - 1
    if (realAge < 18 || realAge > 120) {
      errors.birthDate = t('register.errors.birthDateInvalid')
    } else {
      errors.birthDate = ''
    }
  }

  function validatePassword() {
    errors.password = isPasswordValid.value ? '' : t('register.errors.password')
  }

  function validateConfirm() {
    errors.confirmPassword = form.password !== form.confirmPassword
      ? t('register.errors.confirmPassword') : ''
  }

  // ── Formatação CPF ───────────────────────────────────────────────────────────

  function validateTerms() {
    errors.terms = !form.termsAccepted ? t('register.errors.terms') : ''
  }

  function validatePrivacy() {
    errors.privacy = !form.privacyAccepted ? t('register.errors.privacy') : ''
  }

  // ── Submit ───────────────────────────────────────────────────────────────────

  async function handleRegister() {
    const fields = ['name', 'email', 'birthDate', 'password', 'confirmPassword', 'terms', 'privacy']
    fields.forEach(touch)
    validateName(); validateEmail(); validateBirthDate(); validatePassword(); validateConfirm(); validateTerms(); validatePrivacy()

    if (!isFormValid.value) return

    loading.value  = true
    apiError.value = ''
    try {
      await auth.register({
        name:           form.name,
        email:          form.email,
        password:       form.password,
        birth_date:     form.birthDate || null,
        terms_accepted:   form.termsAccepted,
        privacy_accepted: form.privacyAccepted,
        profile:        { country: form.country },
      })
      registered.value = true
    } catch (e) {
      const status = e.response?.status
      const detail = e.response?.data?.detail || ''

      if (status === 409 && detail.includes('E-mail')) {
        apiError.value = t('register.errors.emailTaken')
      } else {
        apiError.value = t('register.errors.api')
      }
    } finally {
      loading.value = false
    }
  }

  return {
    form, errors, touched, loading, apiError, registered,
    rules, isPasswordValid, isFormValid,
    touch, validateName, validateEmail, validateBirthDate, validatePassword, validateConfirm, validateTerms, validatePrivacy,
    handleRegister,
  }
}