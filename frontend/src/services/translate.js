// src/services/translate.js
import axios from 'axios'

// Pares suportados pelo MyMemory com códigos simples (ISO 639-1)
// MyMemory trata pt como pt-BR internamente quando necessário
const SUPPORTED_LOCALES = new Set(['pt', 'en', 'es'])

/**
 * Traduz um texto usando a MyMemory API (gratuita, sem chave).
 * Sempre traduz do idioma original para o idioma alvo.
 *
 * @param {string} text       - texto a traduzir
 * @param {string} sourceLang - idioma de origem ('pt' | 'en' | 'es')
 * @param {string} targetLang - idioma de destino ('pt' | 'en' | 'es')
 * @returns {Promise<string>} - texto traduzido, ou o original em caso de erro
 */
export async function translateText(text, sourceLang, targetLang) {
  if (!text) return text
  if (sourceLang === targetLang) return text
  if (!SUPPORTED_LOCALES.has(sourceLang) || !SUPPORTED_LOCALES.has(targetLang)) return text

  try {
    const { data } = await axios.get('https://api.mymemory.translated.net/get', {
      params: { q: text, langpair: `${sourceLang}|${targetLang}` },
    })
    return data.responseData?.translatedText || text
  } catch {
    return text
  }
}
