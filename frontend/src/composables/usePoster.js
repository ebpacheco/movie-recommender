// src/composables/usePoster.js
import { searchMovie } from '@/services/tmdb'

function tmdbLocale(lang) {
  return lang === 'pt' ? 'pt-BR' : lang === 'es' ? 'es-ES' : 'en-US'
}

export async function fetchPoster(title, year, lang) {
  return searchMovie(title, year, tmdbLocale(lang))
}
