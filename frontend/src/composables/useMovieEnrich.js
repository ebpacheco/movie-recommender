// src/composables/useMovieEnrich.js
import { watch } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'
import { fetchPoster } from '@/composables/usePoster'
import { fetchRatings } from '@/composables/useRatings'
import { getWatchProviders } from '@/services/tmdb'
export { fetchTrailerKey } from '@/services/youtube'

/**
 * Enriquece lista de filmes com poster, ratings e streaming providers.
 *
 * @param {Array}  list            - filmes brutos da IA
 * @param {string} lang            - idioma ('pt' | 'en' | 'es')
 * @param {object} options
 * @param {string} options.watchRegion      - código ISO do país (ex: 'BR', 'US')
 * @param {Array}  options.userPlatformIds  - IDs das plataformas do usuário
 */
export async function enrichMovies(list, lang, { watchRegion = 'BR', userPlatformIds = null } = {}) {
  const enriched = await Promise.all(
    list.map(async (movie) => {
      const [{ tmdbId, poster, localTitle }, ratings] = await Promise.all([
        fetchPoster(movie.title, movie.year, lang),
        fetchRatings(movie.title, movie.year),
      ])
      const streamingProviders = await getWatchProviders(tmdbId, watchRegion)
      return { ...movie, tmdbId, poster, localTitle, ...ratings, streamingProviders }
    })
  )

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
