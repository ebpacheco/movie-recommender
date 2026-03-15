// src/composables/useRecaptcha.js
const SITE_KEY = import.meta.env.VITE_RECAPTCHA_SITE_KEY

function loadScript() {
  if (document.getElementById('recaptcha-script') || !SITE_KEY) return
  const script = document.createElement('script')
  script.id    = 'recaptcha-script'
  script.src   = `https://www.google.com/recaptcha/api.js?render=${SITE_KEY}`
  script.async = true
  document.head.appendChild(script)
}

function waitReady() {
  return new Promise((resolve) => {
    const check = () => window.grecaptcha?.ready ? window.grecaptcha.ready(resolve) : setTimeout(check, 100)
    check()
  })
}

export function useRecaptcha() {
  loadScript()

  async function executeRecaptcha(action = 'login') {
    if (!SITE_KEY) return ''
    await waitReady()
    return window.grecaptcha.execute(SITE_KEY, { action })
  }

  return { executeRecaptcha }
}
