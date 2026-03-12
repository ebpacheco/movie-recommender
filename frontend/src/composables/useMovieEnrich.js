// src/composables/useMovieEnrich.js
import { watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'

const TMDB_TOKEN    = import.meta.env.VITE_TMDB_TOKEN
const OMDB_KEY      = import.meta.env.VITE_OMDB_API_KEY
const TMDB_IMG_URL  = 'https://image.tmdb.org/t/p/w342'
const TMDB_LOGO_URL = 'https://image.tmdb.org/t/p/w45'

function tmdbLocale(lang) {
  return lang === 'pt' ? 'pt-BR' : lang === 'es' ? 'es-ES' : 'en-US'
}

export async function fetchPoster(title, year, lang) {
  try {
    const { data } = await axios.get('https://api.themoviedb.org/3/search/movie', {
      headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
      params:  { query: title, year: year || undefined, language: tmdbLocale(lang) },
    })
    const result = data.results?.[0]
    return {
      tmdbId:     result?.id || null,
      poster:     result?.poster_path ? `${TMDB_IMG_URL}${result.poster_path}` : null,
      localTitle: result?.title || title,
    }
  } catch { return { tmdbId: null, poster: null, localTitle: title } }
}

export async function fetchRatings(title, year) {
  try {
    const { data } = await axios.get('https://www.omdbapi.com/', {
      params: { apikey: OMDB_KEY, t: title, y: year || undefined, tomatoes: true },
    })
    if (data.Response === 'False') return {}
    const rt = data.Ratings?.find(r => r.Source === 'Rotten Tomatoes')
    return {
      imdb:           data.imdbRating !== 'N/A' ? data.imdbRating : null,
      rottenTomatoes: rt?.Value || null,
    }
  } catch { return {} }
}

export async function fetchTrailerKey(title, year) {
  try {
    const { data: search } = await axios.get('https://api.themoviedb.org/3/search/movie', {
      headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
      params:  { query: title, year: year || undefined },
    })
    const tmdbId = search.results?.[0]?.id
    if (!tmdbId) return null

    const { data: videos } = await axios.get(
      `https://api.themoviedb.org/3/movie/${tmdbId}/videos`,
      { headers: { Authorization: `Bearer ${TMDB_TOKEN}` }, params: { language: 'en-US' } }
    )

    const items = videos.results || []
    const pick =
      items.find(v => v.site === 'YouTube' && v.type === 'Trailer' && v.official) ||
      items.find(v => v.site === 'YouTube' && v.type === 'Trailer') ||
      items.find(v => v.site === 'YouTube' && v.type === 'Teaser') ||
      items.find(v => v.site === 'YouTube')

    return pick?.key || null
  } catch { return null }
}

/**
 * Busca provedores de streaming para um filme em um país específico.
 * Retorna array de { id, name, logo } — flatrate (assinatura) apenas.
 */
export async function fetchStreamingProviders(tmdbId, watchRegion = 'BR') {
  if (!tmdbId) return []
  try {
    const { data } = await axios.get(
      `https://api.themoviedb.org/3/movie/${tmdbId}/watch/providers`,
      { headers: { Authorization: `Bearer ${TMDB_TOKEN}` } }
    )
    const regionData = data.results?.[watchRegion]
    const providers  = regionData?.flatrate || []
    return providers.map(p => ({
      id:   String(p.provider_id),
      name: p.provider_name,
      logo: `${TMDB_LOGO_URL}${p.logo_path}`,
    }))
  } catch { return [] }
}

/**
 * Enriquece lista de filmes com poster, ratings e streaming providers.
 *
 * @param {Array}  list            - filmes brutos da IA
 * @param {string} lang            - idioma ('pt' | 'en' | 'es')
 * @param {object} options
 * @param {string} options.watchRegion      - código ISO do país (ex: 'BR', 'US')
 * @param {Array}  options.userPlatformIds  - IDs das plataformas do usuário (ex: ['8','119'])
 *                                           Se fornecido, filtra filmes não disponíveis
 */
export async function enrichMovies(list, lang, { watchRegion = 'BR', userPlatformIds = null } = {}) {
  const enriched = await Promise.all(
    list.map(async (movie) => {
      const [{ tmdbId, poster, localTitle }, ratings] = await Promise.all([
        fetchPoster(movie.title, movie.year, lang),
        fetchRatings(movie.title, movie.year),
      ])
      const streamingProviders = await fetchStreamingProviders(tmdbId, watchRegion)
      return { ...movie, tmdbId, poster, localTitle, ...ratings, streamingProviders }
    })
  )

  // Filtro estrito: só filmes disponíveis nas plataformas do usuário, pega os 6 primeiros
  if (userPlatformIds?.length) {
    return enriched
      .filter(m => m.streamingProviders.some(p => userPlatformIds.includes(p.id)))
      .slice(0, 6)
  }

  return enriched.slice(0, 6)
}

// Composable que reage à mudança de locale
export function useLocaleTranslation(movies, translating) {
  const { locale } = useI18n()

  watch(() => locale.value, async (newLocale) => {
    if (!movies.value.length) return
    translating.value = true
    try {
      const payload = {
        language: newLocale,
        movies: movies.value.map(m => ({ title: m.title, year: m.year, genre: m.genre })),
      }
      const [translateRes, newPosters] = await Promise.all([
        api.post('/translate', payload),
        Promise.all(movies.value.map(m => fetchPoster(m.title, m.year, newLocale))),
      ])

      movies.value = movies.value.map((movie, i) => ({
        ...movie,
        description: translateRes.data.movies[i]?.description ?? movie.description,
        genre:       translateRes.data.movies[i]?.genre       ?? movie.genre,
        poster:      newPosters[i]?.poster                    ?? movie.poster,
        localTitle:  newPosters[i]?.localTitle                ?? movie.localTitle,
      }))
    } catch {}
    finally { translating.value = false }
  })
}