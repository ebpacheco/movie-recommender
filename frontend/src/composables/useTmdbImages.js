// src/composables/useTmdbImages.js
import axios from 'axios'

const TMDB_TOKEN   = import.meta.env.VITE_TMDB_TOKEN
const TMDB_IMG_URL = 'https://image.tmdb.org/t/p/w92'
const CACHE_KEY    = 'cinemagic_img_cache'

// ── Cache sessionStorage ──────────────────────────────────────────────────────

function cacheGet(key) {
  try {
    const store = JSON.parse(sessionStorage.getItem(CACHE_KEY) || '{}')
    return key in store ? store[key] : undefined
  } catch { return undefined }
}

function cacheSet(key, value) {
  try {
    const store = JSON.parse(sessionStorage.getItem(CACHE_KEY) || '{}')
    store[key] = value
    sessionStorage.setItem(CACHE_KEY, JSON.stringify(store))
  } catch {}
}

async function cachedFetch(key, fetchFn) {
  const cached = cacheGet(key)
  if (cached !== undefined) return cached
  const result = await fetchFn()
  cacheSet(key, result)
  return result
}

// ── Buscas TMDB ───────────────────────────────────────────────────────────────

export async function fetchMovieImage(name) {
  return cachedFetch(`movie:${name}`, async () => {
    try {
      const { data } = await axios.get('https://api.themoviedb.org/3/search/movie', {
        headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
        params:  { query: name, language: 'pt-BR', page: 1 },
      })
      const result = data.results?.[0]
      return result?.poster_path ? `${TMDB_IMG_URL}${result.poster_path}` : null
    } catch { return null }
  })
}

export async function fetchPersonImage(name) {
  return cachedFetch(`person:${name}`, async () => {
    try {
      const { data } = await axios.get('https://api.themoviedb.org/3/search/person', {
        headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
        params:  { query: name, language: 'pt-BR', page: 1 },
      })
      const result = data.results?.[0]
      return result?.profile_path ? `${TMDB_IMG_URL}${result.profile_path}` : null
    } catch { return null }
  })
}

// Converte lista de strings em objetos {id, name, image} buscando fotos em paralelo
export async function enrichItems(names, type = 'person') {
  const fetchFn = type === 'movie' ? fetchMovieImage : fetchPersonImage
  return Promise.all(
    (names || []).map(async (name) => {
      const image = await fetchFn(name)
      return { id: name, name, image }
    })
  )
}