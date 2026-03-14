// src/composables/useMovieEnrich.js
import { watch } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'
import { fetchPoster } from '@/composables/usePoster'
import { fetchRatings } from '@/composables/useRatings'
import { getWatchProviders } from '@/services/tmdb'
import { translateText } from '@/services/translate'
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

  // Posições 1-10 = preferências, 11-20 = curingas
  const preferencePool = enriched.slice(0, 10)
  const curingaPool    = enriched.slice(10)

  function pick3(pool) {
    if (!userPlatformIds?.length) return pool.slice(0, 3)
    const ids = userPlatformIds.map(String)
    const filtered = pool.filter(m => m.streamingProviders.some(p => ids.includes(String(p.id))))
    // fallback: se não houver 3 confirmados, completa com os primeiros do pool
    if (filtered.length >= 3) return filtered.slice(0, 3)
    const fallback = pool.filter(m => !filtered.includes(m)).slice(0, 3 - filtered.length)
    return [...filtered, ...fallback]
  }

  return [...pick3(preferencePool), ...pick3(curingaPool)]
}

/**
 * Composable que reage à mudança de locale.
 * Traduz filmes (descrição, gênero, poster) e a mensagem da IA juntos,
 * garantindo que tudo retorne ao mesmo tempo sob um único flag `translating`.
 *
 * @param {Ref<Array>}  movies
 * @param {Ref<boolean>} translating
 * @param {Ref<string>}  aiMessage         - mensagem atual exibida
 * @param {Ref<string>}  originalAiMessage - mensagem original (idioma de origem)
 * @param {Ref<string>}  originalAiLocale  - idioma em que a mensagem foi gerada
 */
export function useLocaleTranslation(movies, translating, aiMessage, originalAiMessage, originalAiLocale) {
  const { locale } = useI18n()

  watch(() => locale.value, async (newLocale) => {
    if (!movies.value.length) return
    translating.value = true
    try {
      const payload = {
        language: newLocale,
        movies: movies.value.map(m => ({ title: m.title, year: m.year, genre: m.genre })),
      }
      const [translateRes, newPosters, translatedMessage] = await Promise.all([
        api.post('/translate', payload),
        Promise.all(movies.value.map(m => fetchPoster(m.title, m.year, newLocale))),
        aiMessage && originalAiMessage?.value
          ? translateText(originalAiMessage.value, originalAiLocale?.value || newLocale, newLocale)
          : Promise.resolve(null),
      ])

      movies.value = movies.value.map((movie, i) => ({
        ...movie,
        description: translateRes.data.movies[i]?.description ?? movie.description,
        genre:       translateRes.data.movies[i]?.genre       ?? movie.genre,
        poster:      newPosters[i]?.poster                    ?? movie.poster,
        localTitle:  newPosters[i]?.localTitle                ?? movie.localTitle,
      }))

      if (translatedMessage && aiMessage) aiMessage.value = translatedMessage
    } catch {}
    finally { translating.value = false }
  })
}
