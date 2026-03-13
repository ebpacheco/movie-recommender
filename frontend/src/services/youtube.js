// src/services/youtube.js
import { searchMovie, getMovieVideos } from '@/services/tmdb'

export async function fetchTrailerKey(title, year) {
  try {
    const { tmdbId } = await searchMovie(title, year, 'en-US')
    if (!tmdbId) return null

    const items = await getMovieVideos(tmdbId)
    const pick =
      items.find(v => v.site === 'YouTube' && v.type === 'Trailer' && v.official) ||
      items.find(v => v.site === 'YouTube' && v.type === 'Trailer') ||
      items.find(v => v.site === 'YouTube' && v.type === 'Teaser') ||
      items.find(v => v.site === 'YouTube')

    return pick?.key || null
  } catch { return null }
}
