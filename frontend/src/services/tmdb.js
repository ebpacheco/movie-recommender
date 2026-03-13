// src/services/tmdb.js
import axios from 'axios'

const TOKEN = import.meta.env.VITE_TMDB_TOKEN

export const TMDB_BASE = 'https://api.themoviedb.org/3'
export const IMG_W342  = 'https://image.tmdb.org/t/p/w342'
export const IMG_W92   = 'https://image.tmdb.org/t/p/w92'
export const IMG_W45   = 'https://image.tmdb.org/t/p/w45'

const headers = () => ({ Authorization: `Bearer ${TOKEN}` })

// IDs dos populares no Brasil
const POPULAR_IDS = [8, 119, 337, 1899, 531, 350, 307, 619, 167, 584]
const POPULAR_SET = new Set(POPULAR_IDS)
const BLOCKED_IDS = new Set([3, 10, 192, 2, 68, 35, 130, 509, 384, 213])

export async function searchMovieSuggestions(query, language = 'pt-BR') {
  try {
    const { data } = await axios.get(`${TMDB_BASE}/search/movie`, {
      headers: headers(),
      params:  { query, language, page: 1 },
    })
    return data.results || []
  } catch { return [] }
}

export async function searchMovie(query, year, language = 'pt-BR') {
  try {
    const { data } = await axios.get(`${TMDB_BASE}/search/movie`, {
      headers: headers(),
      params:  { query, year: year || undefined, language },
    })
    const result = data.results?.[0]
    return {
      tmdbId:     result?.id || null,
      poster:     result?.poster_path ? `${IMG_W342}${result.poster_path}` : null,
      localTitle: result?.title || query,
    }
  } catch {
    return { tmdbId: null, poster: null, localTitle: query }
  }
}

export async function searchPerson(query, language = 'pt-BR') {
  try {
    const { data } = await axios.get(`${TMDB_BASE}/search/person`, {
      headers: headers(),
      params:  { query, language, page: 1 },
    })
    return data.results || []
  } catch { return [] }
}

export async function getMovieVideos(tmdbId) {
  try {
    const { data } = await axios.get(`${TMDB_BASE}/movie/${tmdbId}/videos`, {
      headers: headers(),
      params:  { language: 'en-US' },
    })
    return data.results || []
  } catch { return [] }
}

export async function getWatchProviders(tmdbId, watchRegion = 'BR') {
  if (!tmdbId) return []
  try {
    const { data } = await axios.get(`${TMDB_BASE}/movie/${tmdbId}/watch/providers`, {
      headers: headers(),
    })
    const providers = data.results?.[watchRegion]?.flatrate || []
    return providers.map(p => ({
      id:   String(p.provider_id),
      name: p.provider_name,
      logo: `${IMG_W45}${p.logo_path}`,
    }))
  } catch { return [] }
}

export async function getAllProviders(watchRegion = 'BR', language = 'pt-BR') {
  const { data } = await axios.get(`${TMDB_BASE}/watch/providers/movie`, {
    headers: headers(),
    params:  { watch_region: watchRegion, language },
  })
  const all = (data.results || [])
    .filter(p => !BLOCKED_IDS.has(p.provider_id))
    .map(p => ({
      id:      String(p.provider_id),
      name:    p.provider_name,
      logo:    `${IMG_W45}${p.logo_path}`,
      popular: POPULAR_SET.has(p.provider_id),
    }))

  const popular = POPULAR_IDS
    .map(id => all.find(p => p.id === String(id)))
    .filter(Boolean)

  const others = all
    .filter(p => !POPULAR_SET.has(Number(p.id)))
    .sort((a, b) => a.name.localeCompare(b.name))

  return { popular, others }
}

export async function searchMovieImage(name) {
  try {
    const { data } = await axios.get(`${TMDB_BASE}/search/movie`, {
      headers: headers(),
      params:  { query: name, language: 'pt-BR', page: 1 },
    })
    const result = data.results?.[0]
    return result?.poster_path ? `${IMG_W92}${result.poster_path}` : null
  } catch { return null }
}

export async function searchPersonImage(name) {
  try {
    const { data } = await axios.get(`${TMDB_BASE}/search/person`, {
      headers: headers(),
      params:  { query: name, language: 'pt-BR', page: 1 },
    })
    const result = data.results?.[0]
    return result?.profile_path ? `${IMG_W92}${result.profile_path}` : null
  } catch { return null }
}
