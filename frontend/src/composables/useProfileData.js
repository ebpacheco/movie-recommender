// src/composables/useProfileData.js
import { ref, reactive } from 'vue'
import api from '@/services/api'
import { enrichItems } from '@/composables/useTmdbImages'

export const GENRE_OPTIONS = [
  { value: 'Ação',               label: 'Ação',               emoji: '💥' },
  { value: 'Aventura',           label: 'Aventura',           emoji: '🗺️' },
  { value: 'Comédia',            label: 'Comédia',            emoji: '😂' },
  { value: 'Drama',              label: 'Drama',              emoji: '🎭' },
  { value: 'Fantasia',           label: 'Fantasia',           emoji: '🧙' },
  { value: 'Ficção Científica',  label: 'Ficção Científica',  emoji: '🚀' },
  { value: 'Terror',             label: 'Terror',             emoji: '👻' },
  { value: 'Mistério',           label: 'Mistério',           emoji: '🔍' },
  { value: 'Suspense / Thriller',label: 'Suspense / Thriller',emoji: '😰' },
  { value: 'Romance',            label: 'Romance',            emoji: '❤️' },
  { value: 'Crime / Policial',   label: 'Crime / Policial',   emoji: '🕵️' },
  { value: 'Guerra',             label: 'Guerra',             emoji: '⚔️' },
  { value: 'Western',            label: 'Western',            emoji: '🤠' },
  { value: 'Histórico / Épico',  label: 'Histórico / Épico',  emoji: '🏛️' },
  { value: 'Musical',            label: 'Musical',            emoji: '🎵' },
  { value: 'Animação',           label: 'Animação',           emoji: '✨' },
  { value: 'Documentário',       label: 'Documentário',       emoji: '📽️' },
  { value: 'Família / Infantil', label: 'Família / Infantil', emoji: '👨‍👩‍👧' },
  { value: 'Biografia',          label: 'Biografia',          emoji: '📖' },
  { value: 'Esporte',            label: 'Esporte',            emoji: '🏆' },
]

export const COUNTRIES = [
  { code: 'BR', name: 'Brasil',          flag: '🇧🇷' },
  { code: 'US', name: 'United States',   flag: '🇺🇸' },
  { code: 'GB', name: 'United Kingdom',  flag: '🇬🇧' },
  { code: 'PT', name: 'Portugal',        flag: '🇵🇹' },
  { code: 'AR', name: 'Argentina',       flag: '🇦🇷' },
  { code: 'MX', name: 'México',          flag: '🇲🇽' },
  { code: 'CO', name: 'Colômbia',        flag: '🇨🇴' },
  { code: 'CL', name: 'Chile',           flag: '🇨🇱' },
  { code: 'PE', name: 'Peru',            flag: '🇵🇪' },
  { code: 'CA', name: 'Canadá',          flag: '🇨🇦' },
  { code: 'AU', name: 'Austrália',       flag: '🇦🇺' },
  { code: 'FR', name: 'França',          flag: '🇫🇷' },
  { code: 'DE', name: 'Alemanha',        flag: '🇩🇪' },
  { code: 'ES', name: 'Espanha',         flag: '🇪🇸' },
  { code: 'IT', name: 'Itália',          flag: '🇮🇹' },
  { code: 'JP', name: 'Japão',           flag: '🇯🇵' },
  { code: 'KR', name: 'Coreia do Sul',   flag: '🇰🇷' },
  { code: 'IN', name: 'Índia',           flag: '🇮🇳' },
]

export function useProfileData() {
  const loading = ref(true)

  const profile = reactive({
    favorite_genres:     [],
    favorite_movies:     [],
    favorite_actors:     [],
    favorite_directors:  [],
    streaming_platforms: [],
    country:             'BR',
  })

  // ── Fetch + enrich ───────────────────────────────────────────────────────────

  async function fetchProfile(onReady) {
    try {
      const { data } = await api.get('/users/me/profile')

      Object.assign(profile, {
        favorite_genres:     data.favorite_genres     || [],
        favorite_movies:     (data.favorite_movies    || []).map(n => ({ id: n, name: n, image: null })),
        favorite_actors:     (data.favorite_actors    || []).map(n => ({ id: n, name: n, image: null })),
        favorite_directors:  (data.favorite_directors || []).map(n => ({ id: n, name: n, image: null })),
        streaming_platforms: data.streaming_platforms || [],
        country:             data.country             || 'BR',
      })

      loading.value = false
      onReady?.()

      const [movies, actors, directors] = await Promise.all([
        enrichItems(data.favorite_movies,    'movie'),
        enrichItems(data.favorite_actors,    'person'),
        enrichItems(data.favorite_directors, 'person'),
      ])

      onReady?.(false)
      profile.favorite_movies    = movies
      profile.favorite_actors    = actors
      profile.favorite_directors = directors
      await new Promise(r => setTimeout(r, 100))
      onReady?.(true)

    } catch (e) {
      console.error('Erro ao carregar perfil', e)
      loading.value = false
      onReady?.()
    }
  }

  // ── Toggles ──────────────────────────────────────────────────────────────────

  function toggleGenre(genre) {
    const idx = profile.favorite_genres.indexOf(genre)
    if (idx >= 0) profile.favorite_genres.splice(idx, 1)
    else if (profile.favorite_genres.length < 3) profile.favorite_genres.push(genre)
  }

  function toggleStreaming(id) {
    const idx = profile.streaming_platforms.indexOf(id)
    if (idx >= 0) profile.streaming_platforms.splice(idx, 1)
    else profile.streaming_platforms.push(id)
  }

  return { profile, loading, fetchProfile, toggleGenre, toggleStreaming }
}