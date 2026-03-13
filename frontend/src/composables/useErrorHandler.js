// src/composables/useErrorHandler.js
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

export function useErrorHandler() {
  const { t } = useI18n()
  const error = ref('')

  function handle(err, fallbackKey = 'errors.generic') {
    error.value = err?.response?.data?.detail || t(fallbackKey)
  }

  function clear() {
    error.value = ''
  }

  return { error, handle, clear }
}
