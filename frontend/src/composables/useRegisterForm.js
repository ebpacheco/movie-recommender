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
    cpf:             '',
    password:        '',
    confirmPassword: '',
    country:         'BR',
    birthDate:       '',
  })

  const errors = reactive({
    name:            '',
    email:           '',
    cpf:             '',
    password:        '',
    confirmPassword: '',
    birthDate:       '',
  })

  const touched = reactive({
    name:            false,
    email:           false,
    cpf:             false,
    password:        false,
    confirmPassword: false,
    birthDate:       false,
  })

  const loading  = ref(false)
  const apiError = ref('')

  // Auto-detecta país ao montar — mantém BR se não detectar nada
  onMounted(async () => {
    const detected = await detectCountry()
    form.country = detected || 'BR'
  })

  // ── Regras de senha ──────────────────────────────────────────────────────────

  const rules = computed(() => ({
    length:  form.password.length >= 8,
    upper:   /[A-Z]/.test(form.password),
    number:  /[0-9]/.test(form.password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(form.password),
  }))

  const isPasswordValid = computed(() => Object.values(rules.value).every(Boolean))

  const isFormValid = computed(() =>
    form.name && form.email && form.cpf && form.birthDate &&
    isPasswordValid.value &&
    form.password === form.confirmPassword &&
    !Object.values(errors).some(Boolean)
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

  function validateCpf() {
    errors.cpf = form.cpf.replace(/\D/g, '').length !== 11
      ? t('register.errors.cpf') : ''
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
    if (realAge < 10 || realAge > 120) {
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

  function formatCpf() {
    let v = form.cpf.replace(/\D/g, '')
    if      (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{0,2})/, '$1.$2.$3-$4')
    else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{0,3})/, '$1.$2.$3')
    else if (v.length > 3) v = v.replace(/(\d{3})(\d{0,3})/, '$1.$2')
    form.cpf = v
    touched.cpf && validateCpf()
  }

  // ── Submit ───────────────────────────────────────────────────────────────────

  async function handleRegister() {
    const fields = ['name', 'email', 'cpf', 'birthDate', 'password', 'confirmPassword']
    fields.forEach(touch)
    validateName(); validateEmail(); validateCpf(); validateBirthDate(); validatePassword(); validateConfirm()

    if (!isFormValid.value) return

    loading.value  = true
    apiError.value = ''
    try {
      await auth.register({
        name:       form.name,
        email:      form.email,
        cpf:        form.cpf.replace(/\D/g, ''),
        password:   form.password,
        birth_date: form.birthDate || null,
        profile:    { country: form.country },
      })
      router.push('/recommendations')
    } catch (e) {
      apiError.value = e.response?.data?.detail || t('register.errors.api')
    } finally {
      loading.value = false
    }
  }

  return {
    form, errors, touched, loading, apiError,
    rules, isPasswordValid, isFormValid,
    touch, validateName, validateEmail, validateCpf, validateBirthDate, validatePassword, validateConfirm,
    formatCpf, handleRegister,
  }
}