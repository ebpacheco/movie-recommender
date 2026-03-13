// src/services/omdb.js
import axios from 'axios'

const API_KEY = import.meta.env.VITE_OMDB_API_KEY

export async function fetchRatings(title, year) {
  try {
    const { data } = await axios.get('https://www.omdbapi.com/', {
      params: { apikey: API_KEY, t: title, y: year || undefined, tomatoes: true },
    })
    if (data.Response === 'False') return {}
    const rt = data.Ratings?.find(r => r.Source === 'Rotten Tomatoes')
    return {
      imdb:           data.imdbRating !== 'N/A' ? data.imdbRating : null,
      rottenTomatoes: rt?.Value || null,
    }
  } catch { return {} }
}
