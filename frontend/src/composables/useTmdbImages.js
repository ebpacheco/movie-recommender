// src/composables/useTmdbImages.js
import { searchMovieImage, searchPersonImage } from '@/services/tmdb'

const CACHE_KEY = 'cinemagic_img_cache'

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
  return cachedFetch(`movie:${name}`, () => searchMovieImage(name))
}

export async function fetchPersonImage(name) {
  return cachedFetch(`person:${name}`, () => searchPersonImage(name))
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
