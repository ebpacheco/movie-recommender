// src/composables/useCountryDetect.js

/**
 * Detecta o país do usuário via IP (ipapi.co).
 * Fallback: extrai do locale do browser (ex: pt-BR → BR).
 * Retorna código ISO 3166-1 alpha-2 (ex: 'BR', 'US').
 */
export async function detectCountry() {
  try {
    const res = await fetch('https://ipapi.co/country/', { signal: AbortSignal.timeout(3000) })
    if (res.ok) {
      const code = (await res.text()).trim()
      if (/^[A-Z]{2}$/.test(code)) return code
    }
  } catch {}

  // Fallback: navigator.language → 'pt-BR' → 'BR'
  const locale = navigator.language || navigator.languages?.[0] || 'en-US'
  const parts  = locale.split('-')
  return parts.length > 1 ? parts[1].toUpperCase() : 'US'
}