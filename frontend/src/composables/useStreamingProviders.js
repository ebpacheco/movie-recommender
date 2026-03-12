// src/composables/useStreamingProviders.js
import { ref, computed } from 'vue'
import axios from 'axios'

const TMDB_TOKEN    = import.meta.env.VITE_TMDB_TOKEN
const TMDB_LOGO_URL = 'https://image.tmdb.org/t/p/w45'
const CACHE_KEY     = 'cinemagic_providers_cache'

// IDs dos populares no Brasil — aparecem em destaque e em ordem
const POPULAR_IDS = [
  8,    // Netflix
  119,  // Amazon Prime Video
  337,  // Disney+
  1899, // Max (HBO Max)
  531,  // Paramount+
  350,  // Apple TV+
  307,  // Globoplay
  619,  // Star+
  167,  // Mubi
  584,  // Pluto TV BR (substitui Claro Video)
]

const POPULAR_SET = new Set(POPULAR_IDS)

// IDs irrelevantes (aluguel/compra avulsa)
const BLOCKED_IDS = new Set([3, 10, 192, 2, 68, 35, 130, 509, 384, 213])  // inclui Claro Video

let _promise = null

export async function fetchAllProviders() {
  try {
    const cached = sessionStorage.getItem(CACHE_KEY)
    if (cached) return JSON.parse(cached)
  } catch {}

  if (!_promise) {
    _promise = axios.get('https://api.themoviedb.org/3/watch/providers/movie', {
      headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
      params:  { watch_region: 'BR', language: 'pt-BR' },
    }).then(({ data }) => {
      const all = (data.results || [])
        .filter(p => !BLOCKED_IDS.has(p.provider_id))
        .map(p => ({
          id:       String(p.provider_id),
          name:     p.provider_name,
          logo:     `${TMDB_LOGO_URL}${p.logo_path}`,
          popular:  POPULAR_SET.has(p.provider_id),
        }))

      // Populares na ordem definida, outros em ordem alfabética
      const popular = POPULAR_IDS
        .map(id => all.find(p => p.id === String(id)))
        .filter(Boolean)

      const others = all
        .filter(p => !POPULAR_SET.has(Number(p.id)))
        .sort((a, b) => a.name.localeCompare(b.name))

      const result = { popular, others }
      try { sessionStorage.setItem(CACHE_KEY, JSON.stringify(result)) } catch {}
      return result
    }).finally(() => { _promise = null })
  }

  return _promise
}

export function useStreamingProviders() {
  const popular = ref([])
  const others  = ref([])
  const loading = ref(true)

  fetchAllProviders()
    .then(({ popular: p, others: o }) => {
      popular.value = p
      others.value  = o
    })
    .catch(() => {})
    .finally(() => { loading.value = false })

  return { popular, others, loading }
}