// src/services/omdb.js
import axios from 'axios'

const API_KEY = import.meta.env.VITE_OMDB_API_KEY

export async function fetchRatings(title, year) {
  try {
    const { data } = await axios.get('https://www.omdbapi.com/', {
      params: { apikey: API_KEY, t: title, y: year || undefined, tomatoes: true },
    })
    if (data.Response === 'False') return {}
    return {
      imdb:     data.imdbRating !== 'N/A' ? data.imdbRating : null,
      runtime:  data.Runtime    !== 'N/A' ? data.Runtime    : null,
    }
  } catch { return {} }
}
