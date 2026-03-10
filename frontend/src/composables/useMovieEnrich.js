// src/composables/useMovieEnrich.js
import { ref, watch } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'

const TMDB_TOKEN   = import.meta.env.VITE_TMDB_TOKEN
const OMDB_KEY     = import.meta.env.VITE_OMDB_API_KEY
const TMDB_IMG_URL = 'https://image.tmdb.org/t/p/w342'

function tmdbLocale(lang) {
  return lang === 'pt' ? 'pt-BR' : lang === 'es' ? 'es-ES' : 'en-US'
}

export async function fetchPoster(title, year, lang) {
  try {
    const { data } = await axios.get('https://api.themoviedb.org/3/search/movie', {
      headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
      params: { query: title, year: year || undefined, language: tmdbLocale(lang) },
    })
    const result = data.results?.[0]
    return {
      poster:     result?.poster_path ? `${TMDB_IMG_URL}${result.poster_path}` : null,
      localTitle: result?.title       || title,
    }
  } catch { return { poster: null, localTitle: title } }
}

export async function fetchRatings(title, year) {
  try {
    const { data } = await axios.get('https://www.omdbapi.com/', {
      params: { apikey: OMDB_KEY, t: title, y: year || undefined, tomatoes: true },
    })
    if (data.Response === 'False') return {}
    const rt = data.Ratings?.find(r => r.Source === 'Rotten Tomatoes')
    return {
      imdb:          data.imdbRating !== 'N/A' ? data.imdbRating : null,
      rottenTomatoes: rt?.Value || null,
    }
  } catch { return {} }
}

export async function fetchTrailerKey(title, year) {
  try {
    const { data: search } = await axios.get('https://api.themoviedb.org/3/search/movie', {
      headers: { Authorization: `Bearer ${TMDB_TOKEN}` },
      params: { query: title, year: year || undefined },
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

export async function enrichMovies(list, lang) {
  return Promise.all(
    list.map(async (movie) => {
      const [{ poster, localTitle }, ratings] = await Promise.all([
        fetchPoster(movie.title, movie.year, lang),
        fetchRatings(movie.title, movie.year),
      ])
      return { ...movie, poster, localTitle, ...ratings }
    })
  )
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