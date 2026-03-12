// src/composables/useTrailer.js
import { ref, onUnmounted } from 'vue'
import { fetchTrailerKey } from '@/composables/useMovieEnrich'

export function useTrailer() {
  const trailerOpen    = ref(false)
  const trailerLoading = ref(false)
  const trailerKey     = ref(null)
  const activeMovie    = ref(null)

  async function openTrailer(movie) {
    activeMovie.value    = movie
    trailerKey.value     = null
    trailerLoading.value = true
    trailerOpen.value    = true
    document.body.style.overflow = 'hidden'
    trailerKey.value     = await fetchTrailerKey(movie.title, movie.year)
    trailerLoading.value = false
  }

  function closeTrailer() {
    trailerOpen.value            = false
    trailerKey.value             = null
    activeMovie.value            = null
    document.body.style.overflow = ''
  }

  function handleKeydown(e) {
    if (e.key === 'Escape' && trailerOpen.value) closeTrailer()
  }

  window.addEventListener('keydown', handleKeydown)
  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
    document.body.style.overflow = ''
  })

  return { trailerOpen, trailerLoading, trailerKey, activeMovie, openTrailer, closeTrailer }
}