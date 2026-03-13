import { createI18n } from 'vue-i18n'
import pt from './locales/pt.json'
import en from './locales/en.json'
import es from './locales/es.json'

const appName = import.meta.env.VITE_APP_NAME || 'CineMagIA'

function detectLanguage() {
  const saved = localStorage.getItem('language')
  if (saved) return saved
  const browser = navigator.language?.slice(0, 2)
  return ['pt', 'en', 'es'].includes(browser) ? browser : 'pt'
}

const i18n = createI18n({
  legacy: false,
  locale: detectLanguage(),
  fallbackLocale: 'pt',
  messages: { pt, en, es },
})

// Injeta o nome do app em todos os locales dinamicamente
;['pt', 'en', 'es'].forEach(lang => {
  i18n.global.mergeLocaleMessage(lang, {
    login: { title: appName },
  })
})

export default i18n

export function setLanguage(lang) {
  i18n.global.locale.value = lang
  localStorage.setItem('language', lang)
  document.documentElement.lang = lang
}

export function getLanguage() {
  return i18n.global.locale.value
}

export { appName }